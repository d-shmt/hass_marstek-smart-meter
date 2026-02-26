"""API for Marstek CT Meter."""
import socket
import logging
import time

_LOGGER = logging.getLogger(__name__)

SOH = 0x01
STX = 0x02
ETX = 0x03

RESPONSE_LABELS = (
    "meter_dev_type",
    "meter_mac_code",
    "hhm_dev_type",
    "hhm_mac_code",
    "A_phase_power",
    "B_phase_power",
    "C_phase_power",
    "total_power",
    "A_chrg_nb",
    "B_chrg_nb",
    "C_chrg_nb",
    "ABC_chrg_nb",
    "wifi_rssi",
    "info_idx",
    "x_chrg_power",
    "A_chrg_power",
    "B_chrg_power",
    "C_chrg_power",
    "ABC_chrg_power",
    "x_dchrg_power",
    "A_dchrg_power",
    "B_dchrg_power",
    "C_dchrg_power",
    "ABC_dchrg_power",
)


class MarstekCtApi:
    """API to communicate with the Marstek CT meter."""

    def __init__(self, host, device_type, battery_mac, ct_mac, ct_type):
        self._host = host
        self._port = 12345
        self._device_type = device_type
        self._battery_mac = battery_mac
        self._ct_mac = ct_mac
        self._ct_type = ct_type

        # Netzwerk- / Retry-Parameter (bewusst konservativ)
        self._timeout = 3.0          # Sekunden pro Versuch
        self._retries = 3            # max. Versuche
        self._retry_delay = 0.3      # Sekunden Pause zwischen Versuchen

        self._payload = self._build_payload()

    def _build_payload(self) -> bytes:
        """Builds the UDP payload for the query."""
        SEPARATOR = "|"
        message_fields = [
            self._device_type,
            self._battery_mac,
            self._ct_type,
            self._ct_mac,
            "0",
            "0",
        ]
        message_bytes = (SEPARATOR + SEPARATOR.join(message_fields)).encode("ascii")

        # Frame: SOH STX <len_ascii> <message_bytes> ETX <xor_hex_2>
        base_size_without_len = 1 + 1 + len(message_bytes) + 1 + 2  # SOH+STX + msg + ETX + xor(2)

        length_str = str(base_size_without_len + len(str(base_size_without_len)))
        while True:
            total_length = base_size_without_len + len(length_str)
            new_length_str = str(total_length)
            if new_length_str == length_str:
                break
            length_str = new_length_str

        payload = bytearray([SOH, STX])
        payload.extend(length_str.encode("ascii"))
        payload.extend(message_bytes)
        payload.append(ETX)

        xor_val = 0
        for b in payload:
            xor_val ^= b
        payload.extend(f"{xor_val:02x}".encode("ascii"))

        return bytes(payload)

    def _extract_message_ascii(self, data: bytes) -> str:
        """Extract the ascii message between the first '|' and ETX."""
        try:
            etx_pos = data.index(bytes([ETX]))
        except ValueError as exc:
            raise ValueError("ETX not found in response") from exc

        frame = data[:etx_pos]
        try:
            pipe_pos = frame.index(b"|")
        except ValueError as exc:
            raise ValueError("No '|' separator found in response") from exc

        msg_bytes = frame[pipe_pos:]
        return msg_bytes.decode("ascii")

    def _decode_response(self, data: bytes) -> dict:
        """Parses the UDP response."""
        try:
            message = self._extract_message_ascii(data)
        except (UnicodeDecodeError, ValueError) as e:
            return {"error": f"Invalid response format: {e}"}

        fields = message.split("|")[1:]

        parsed: dict[str, object] = {}
        for label, val in zip(RESPONSE_LABELS, fields):
            if val == "":
                parsed[label] = None
                continue
            try:
                parsed[label] = int(val)
            except ValueError:
                parsed[label] = val

        if len(fields) < len(RESPONSE_LABELS):
            for label in RESPONSE_LABELS[len(fields):]:
                parsed[label] = None

        self._apply_power_fallback(parsed)

        return parsed

    def _apply_power_fallback(self, parsed: dict[str, object]) -> None:
        """Derive total charge/discharge power when some firmwares report only signed phase/total power."""
        abc_charge = parsed.get("ABC_chrg_power")
        abc_discharge = parsed.get("ABC_dchrg_power")

        if abc_charge is None or abc_discharge is None:
            return
        if abc_charge != 0 or abc_discharge != 0:
            return

        phase_values = [parsed.get("A_phase_power"), parsed.get("B_phase_power"), parsed.get("C_phase_power")]
        phase_numbers = [int(value) for value in phase_values if isinstance(value, int)]

        if phase_numbers and any(value != 0 for value in phase_numbers):
            parsed["ABC_chrg_power"] = sum(max(value, 0) for value in phase_numbers)
            parsed["ABC_dchrg_power"] = sum(max(-value, 0) for value in phase_numbers)
            return

        total_power = parsed.get("total_power")
        if isinstance(total_power, int):
            parsed["ABC_chrg_power"] = max(total_power, 0)
            parsed["ABC_dchrg_power"] = max(-total_power, 0)

    def fetch_data(self) -> dict:
        """Fetch data from the meter with controlled retry (blocking)."""
        last_error = None

        for attempt in range(1, self._retries + 1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                    sock.settimeout(self._timeout)
                    sock.sendto(self._payload, (self._host, self._port))
                    response, _ = sock.recvfrom(2048)
                return self._decode_response(response)

            except socket.timeout:
                last_error = "Timeout - No response from meter"
                _LOGGER.debug(
                    "Marstek CT timeout (attempt %d/%d, timeout=%.1fs)",
                    attempt,
                    self._retries,
                    self._timeout,
                )

            except Exception as e:
                last_error = f"Unexpected error: {e}"
                _LOGGER.warning(
                    "Marstek CT unexpected error on attempt %d/%d: %s",
                    attempt,
                    self._retries,
                    e,
                )

            if attempt < self._retries:
                time.sleep(self._retry_delay)

        return {"error": last_error}

    def test_connection(self) -> dict:
        """A simple blocking call to test connectivity."""
        return self.fetch_data()


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""
