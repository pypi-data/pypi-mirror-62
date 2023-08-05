import typing

from minadb.utils import run_cmd


class ADBClient(object):
    def devices(self) -> typing.List[typing.List[str]]:
        output = str(run_cmd(["adb", "devices"]))
        raw_device_list = [each.split("\t") for each in output.split("\n")[1:] if each]

        # [['123456E', 'device'], ['123456F', 'offline']]
        return raw_device_list

    def available_devices(self) -> typing.List[typing.List[str]]:
        device_list = self.devices()
        return [each for each in device_list if each[1] == "device"]

    def is_device_available(self, serial_no: str) -> bool:
        return serial_no in [each[0] for each in self.available_devices()]


if __name__ == "__main__":
    cli = ADBClient()
    d = cli.available_devices()
    print(d)
    a = cli.is_device_available("123456F")
    print(a)
