"""API for Marstek CT Meter."""
import socket
import re
import logging

_LOGGER = logging.getLogger(__name__)

class MarstekCtApi:
    """API to communicate with the Marstek CT meter."""

    def __init__(self, host, device_type, battery_mac, ct_mac, ct_type):
        self._host = host
        self._port = 12345
        self._device_type = device_type
        self._battery_mac = battery_mac
        self._ct_mac = ct_mac
        self._ct_type = ct_type
        self._timeout = 5.0
        self._payload = self._build_payload()

    def _build_payload(self):
        """Builds the UDP payload for the query."""
        SOH, STX, ETX, SEPARATOR = 0x01, 0x02, 0x03, '|'
        message_fields = [self._device_type, self._battery_mac, self._ct_type, self._ct_mac, '0', '0']
        message_bytes = (SEPARATOR + SEPARATOR.join(message_fields)).encode('ascii')
        base_size = 1 + 1 + len(message_bytes) + 1 + 2
        total_length = base_size + len(str(base_size + 2))
        if len(str(total_length)) != len(str(base_size + 2)):
             total_length = base_size + len(str(total_length))
        payload = bytearray([SOH, STX])
        payload.extend(str(total_length).encode('ascii'))
        payload.extend(message_bytes)
        payload.append(ETX)
        xor = 0
        for b in payload: xor ^= b
        payload.extend(f"{xor:02x}".encode('ascii'))
        return payload

    def _decode_response(self, data: bytes):
        """Parses the UDP response."""
        try:
            message = data[4:-3].decode('ascii')
        except UnicodeDecodeError:
            return {"error": "Invalid ASCII encoding"}
        fields = message.split('|')[1:]

        # KORREKTUR: Wir verwenden wieder die volle Label-Liste, um die richtige Position der Werte zu gewährleisten.
        labels = [
            "meter_dev_type", "meter_mac_code", "hhm_dev_type", "hhm_mac_code",
            "A_phase_power", "B_phase_power", "C_phase_power", "total_power",
            "A_chrg_nb", "B_chrg_nb", "C_chrg_nb", "ABC_chrg_nb", "wifi_rssi",
            "info_idx", "x_chrg_power", "A_chrg_power", "B_chrg_power", "C_chrg_power",
            "ABC_chrg_power", "x_dchrg_power", "A_dchrg_power", "B_dchrg_power",
            "C_dchrg_power", "ABC_dchrg_power"
        ]

        parsed = {}
        for i, label in enumerate(labels):
            val = fields[i] if i < len(fields) else None
            try:
                parsed[label] = int(val)
            except (ValueError, TypeError):
                parsed[label] = val

        # Invertiere den Wert für Phase A, falls nötig
        if "A_phase_power" in parsed and isinstance(parsed["A_phase_power"], int):
            parsed["A_phase_power"] *= -1

        return parsed

    def fetch_data(self):
        """Fetch data from the meter. This is a blocking call."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self._timeout)
        try:
            sock.sendto(self._payload, (self._host, self._port))
            response, _ = sock.recvfrom(1024)
            return self._decode_response(response)
        except socket.timeout:
            return {"error": "Timeout - No response from meter"}
        except Exception as e:
            _LOGGER.warning("An unexpected error occurred: %s", str(e))
            return {"error": f"An unexpected error occurred: {str(e)}"}
        finally:
            sock.close()

    def test_connection(self):
        """A simple blocking call to test connectivity."""
        return self.fetch_data()

class CannotConnect(Exception):
    """Error to indicate we cannot connect."""
class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""
