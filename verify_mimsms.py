import asyncio
import os
import sys

# Ensure local source is in path
sys.path.insert(0, os.path.abspath("src"))

try:
    from rich.console import Console
    from rich.prompt import Prompt
    from rich.status import Status
    from rich.table import Table
except ImportError:
    print("Error: 'rich' library not found. Please install it with 'pip install rich'.")
    sys.exit(1)

from django_mimsms.client import MiMSMSClient

console = Console()


class LiveTester:
    def __init__(self):
        self.results = []
        self.username = ""
        self.apikey = ""
        self.sender = ""
        self.receiver = ""
        self.message = ""
        self.sent_trxn_id = None

    def get_inputs(self):
        console.rule("[bold blue]MiMSMS Live Integration Tester")
        self.username = Prompt.ask("Enter MIMSMS_USERNAME", default=os.getenv("MIMSMS_USERNAME", ""))
        self.apikey = Prompt.ask("Enter MIMSMS_APIKEY", password=True, default=os.getenv("MIMSMS_APIKEY", ""))
        self.sender = Prompt.ask("Enter MIMSMS_SENDER", default=os.getenv("MIMSMS_SENDER", ""))
        self.receiver = Prompt.ask("Enter receiver phone number (optional, e.g. 88017...)", default="")
        self.message = Prompt.ask("Enter test message (optional)", default="Live test from django-mimsms")

        if not all([self.username, self.apikey, self.sender]):
            console.print("[red]Error: Username, Apikey, and Sender are required.[/red]")
            sys.exit(1)

    def log_result(self, endpoint: str, method: str, success: bool, detail: str = ""):
        self.results.append(
            {"endpoint": endpoint, "method": method, "status": "✅ PASS" if success else "❌ FAIL", "detail": detail}
        )

    async def run_tests(self):
        client = MiMSMSClient(username=self.username, apikey=self.apikey, sender_name=self.sender)

        with Status("[bold green]Testing API endpoints..."):
            # 1. Balance Check (POST)
            try:
                bal = client.check_balance()
                self.log_result("Balance Check", "POST", True, f"Balance: {bal}")
            except Exception as e:
                self.log_result("Balance Check", "POST", False, str(e))

            # 2. Balance Check (GET)
            try:
                bal = client.check_balance_get()
                self.log_result("Balance Check", "GET", True, f"Balance: {bal}")
            except Exception as e:
                self.log_result("Balance Check", "GET", False, str(e))

            if self.receiver:
                # 3. Send Single SMS (POST)
                try:
                    res = client.send_sms(number=self.receiver, message=self.message)
                    self.log_result("Send SMS", "POST", True, f"TrxnID: {res.trxn_id}")
                    if not self.sent_trxn_id:
                        self.sent_trxn_id = res.trxn_id
                except Exception as e:
                    self.log_result("Send SMS", "POST", False, str(e))

                # 4. Send Single SMS (GET)
                try:
                    res = client.send_sms_get(number=self.receiver, message=f"{self.message} (GET)")
                    self.log_result("Send SMS", "GET", True, f"TrxnID: {res.trxn_id}")
                    if not self.sent_trxn_id:
                        self.sent_trxn_id = res.trxn_id
                except Exception as e:
                    self.log_result("Send SMS", "GET", False, str(e))

                # 5. Send Bulk SMS (POST)
                try:
                    res = client.send_one_to_many(numbers=[self.receiver], message=f"{self.message} (Bulk)")
                    self.log_result("Bulk SMS", "POST", True, f"TrxnID: {res.trxn_id}")
                    if not self.sent_trxn_id:
                        self.sent_trxn_id = res.trxn_id
                except Exception as e:
                    self.log_result("Bulk SMS", "POST", False, str(e))

                # 6. Send Bulk SMS (GET)
                try:
                    res = client.send_one_to_many_get(numbers=self.receiver, message=f"{self.message} (Bulk GET)")
                    self.log_result("Bulk SMS", "GET", True, f"TrxnID: {res.trxn_id}")
                    if not self.sent_trxn_id:
                        self.sent_trxn_id = res.trxn_id
                except Exception as e:
                    self.log_result("Bulk SMS", "GET", False, str(e))

                # 7. Dynamic SMS (POST)
                try:
                    messages = [{"number": self.receiver, "text": f"{self.message} (Dynamic)"}]
                    res = client.send_dynamic_sms(messages=messages)
                    self.log_result("Dynamic SMS", "POST", True, f"TrxnID: {res.trxn_id}")
                except Exception as e:
                    self.log_result("Dynamic SMS", "POST", False, str(e))

                # 8. Check DLR
                if self.sent_trxn_id:
                    try:
                        res = client.check_dlr(trxn_id=self.sent_trxn_id, number=self.receiver)
                        self.log_result("DLR Check", "POST", True, f"Status: {res.response_result}")
                    except Exception as e:
                        self.log_result("DLR Check", "POST", False, str(e))
                else:
                    self.log_result("DLR Check", "GET", False, "Skipped: No TrxnID from previous tests")
            else:
                self.log_result("SMS Sending", "ALL", False, "Skipped: No receiver phone number provided")

        client.close()

    def print_report(self):
        table = Table(title="MiMSMS Live Test Report", show_header=True, header_style="bold magenta")
        table.add_column("Endpoint", style="dim")
        table.add_column("Method")
        table.add_column("Status")
        table.add_column("Detail", overflow="fold")

        for r in self.results:
            table.add_row(r["endpoint"], r["method"], r["status"], r["detail"])

        console.print("\n")
        console.print(table)
        console.print(
            "\n[bold yellow]Note:[/bold yellow] Tests that involve \
            sending SMS incur costs according to your MiMSMS plan."
        )


async def main():
    tester = LiveTester()
    tester.get_inputs()
    await tester.run_tests()
    tester.print_report()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Test cancelled by user.[/yellow]")
