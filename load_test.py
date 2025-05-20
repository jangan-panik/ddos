import asyncio
import aiohttp
import time
import argparse
import statistics
from dataclasses import dataclass
from typing import List
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, MofNCompleteColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

console = Console()

@dataclass
class TestResult:
    status_code: int
    response_time: float
    error: str = None

class LoadTester:
    def __init__(self):
        self.results = []
        self.start_time = None
        self.console = Console()
        
    def print_banner(self):
        banner = """
 ███████ ███████  ██████  ██     ██  ██████  ████████ ██   ██  █████  
 ██      ██      ██    ██ ██     ██ ██    ██    ██    ██   ██ ██   ██ 
 ███████ █████   ██    ██ ██  █  ██ ██    ██    ██    ███████  █████  
      ██ ██      ██    ██ ██ ███ ██ ██    ██    ██         ██ ██   ██ 
 ███████ ███████  ██████   ███ ███   ██████     ██         ██  █████  
                                                                      
         ⚡ HIGH PERFORMANCE LOAD TESTER ⚡                           
        """
        
        self.console.print(Panel(
            Align.center(Text(banner, style="bold cyan")),
            title="SEOWOT48 LOAD TESTER",
            border_style="bright_cyan",
            box=box.DOUBLE
        ))
    
    async def make_request(self, session: aiohttp.ClientSession, url: str, method: str = 'GET', data: dict = None) -> TestResult:
        start_time = time.time()
        try:
            async with session.request(method, url, json=data, ssl=False) as response:
                await response.text()
                response_time = time.time() - start_time
                return TestResult(response.status, response_time)
        except Exception as e:
            response_time = time.time() - start_time
            return TestResult(0, response_time, str(e))

    def print_test_config(self, url: str, num_requests: int, concurrent_users: int, method: str):
        config_table = Table(title="🚀 Test Configuration", box=box.ROUNDED, border_style="bright_yellow")
        config_table.add_column("Parameter", style="bold white", justify="left")
        config_table.add_column("Value", style="bright_green", justify="left")
        
        config_table.add_row("🎯 Target URL", url)
        config_table.add_row("📊 Total Requests", f"{num_requests:,}")
        config_table.add_row("👥 Concurrent Users", f"{concurrent_users}")
        config_table.add_row("🔨 HTTP Method", method)
        config_table.add_row("⚡ Engine", "SEOWOT48 AsyncIO")
        
        self.console.print(config_table)
        
    def create_progress_bar(self, total_requests: int):
        return Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=50, style="bright_cyan", complete_style="bright_green"),
            MofNCompleteColumn(),
            TextColumn("[bold green]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console
        )

    async def run_load_test(self, url: str, num_requests: int, concurrent_users: int, method: str = 'GET', data: dict = None):
        self.print_banner()
        self.print_test_config(url, num_requests, concurrent_users, method)
        
        connector = aiohttp.TCPConnector(limit=concurrent_users * 2, limit_per_host=concurrent_users)
        timeout = aiohttp.ClientTimeout(total=60)
        
        with self.create_progress_bar(num_requests) as progress:
            task = progress.add_task("🔥 Bombing server...", total=num_requests)
            
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                self.start_time = time.time()
                
                semaphore = asyncio.Semaphore(concurrent_users)
                
                async def bounded_request():
                    async with semaphore:
                        result = await self.make_request(session, url, method, data)
                        self.results.append(result)
                        progress.advance(task)
                        return result
                
                tasks = [bounded_request() for _ in range(num_requests)]
                await asyncio.gather(*tasks)
        
        self.print_final_report()

    def print_final_report(self):
        total_time = time.time() - self.start_time
        
        success_results = [r for r in self.results if r.status_code == 200]
        error_results = [r for r in self.results if r.status_code != 200]
        
        response_times = [r.response_time for r in success_results] if success_results else [0]
        
        self.console.print("\n")
        
        summary_table = Table(title="⚡ SEOWOT48 Performance Report", box=box.DOUBLE_EDGE, border_style="bright_magenta")
        summary_table.add_column("Metric", style="bold white", justify="left")
        summary_table.add_column("Value", style="bright_green", justify="right")
        summary_table.add_column("Status", style="bold yellow", justify="center")
        
        rps = len(self.results) / total_time
        success_rate = (len(success_results) / len(self.results)) * 100 if self.results else 0
        
        summary_table.add_row("🕐 Total Time", f"{total_time:.2f}s", "✅")
        summary_table.add_row("🚀 Requests/Second", f"{rps:.2f}", "⚡" if rps > 100 else "🔥")
        summary_table.add_row("✅ Successful Requests", f"{len(success_results):,}", "💚")
        summary_table.add_row("❌ Failed Requests", f"{len(error_results):,}", "💔" if error_results else "✨")
        summary_table.add_row("📈 Success Rate", f"{success_rate:.1f}%", "🎯" if success_rate > 95 else "⚠️")
        
        if response_times:
            summary_table.add_row("⚡ Min Response", f"{min(response_times)*1000:.0f}ms", "🏃‍♂️")
            summary_table.add_row("📊 Avg Response", f"{statistics.mean(response_times)*1000:.0f}ms", "📈")
            summary_table.add_row("🐌 Max Response", f"{max(response_times)*1000:.0f}ms", "🐢")
            summary_table.add_row("📐 95th Percentile", f"{statistics.quantiles(response_times, n=20)[18]*1000:.0f}ms", "📏")
        
        self.console.print(summary_table)
        
        if error_results:
            self.print_error_breakdown(error_results)
        
        self.print_performance_verdict(success_rate, rps, statistics.mean(response_times) if response_times else 0)

    def print_error_breakdown(self, error_results):
        error_table = Table(title="💥 Error Breakdown", box=box.ROUNDED, border_style="red")
        error_table.add_column("Status Code", style="bold red")
        error_table.add_column("Count", style="bright_red", justify="right")
        error_table.add_column("Percentage", style="yellow", justify="right")
        
        error_counts = {}
        for result in error_results:
            code = result.status_code if result.status_code != 0 else "Connection Error"
            error_counts[code] = error_counts.get(code, 0) + 1
        
        total_errors = len(error_results)
        for code, count in sorted(error_counts.items()):
            percentage = (count / total_errors) * 100
            error_table.add_row(str(code), f"{count:,}", f"{percentage:.1f}%")
        
        self.console.print(error_table)

    def print_performance_verdict(self, success_rate, rps, avg_response_time):
        if success_rate >= 99 and rps >= 1000 and avg_response_time < 0.1:
            verdict = "🔥 LEGENDARY PERFORMANCE! Server is BULLETPROOF! 🔥"
            style = "bold green on black"
        elif success_rate >= 95 and rps >= 500:
            verdict = "⚡ EXCELLENT! Server handles load like a BOSS! ⚡"
            style = "bold bright_green"
        elif success_rate >= 90 and rps >= 100:
            verdict = "👍 GOOD! Server is solid under pressure! 👍"
            style = "bold yellow"
        elif success_rate >= 80:
            verdict = "⚠️  FAIR! Server struggles but survives! ⚠️"
            style = "bold bright_yellow"
        else:
            verdict = "💥 CRITICAL! Server is getting DESTROYED! 💥"
            style = "bold red"
        
        self.console.print("\n")
        self.console.print(Panel(
            Align.center(Text(verdict, style=style)),
            title="🎯 SEOWOT48 VERDICT",
            border_style="bright_cyan",
            box=box.DOUBLE
        ))

def main():
    parser = argparse.ArgumentParser(description='🚀 SEOWOT48 - High Performance Load Tester')
    parser.add_argument('url', help='🎯 Target URL to obliterate')
    parser.add_argument('-n', '--requests', type=int, default=1000, help='📊 Total requests (default: 1000)')
    parser.add_argument('-c', '--concurrent', type=int, default=50, help='👥 Concurrent users (default: 50)')
    parser.add_argument('-m', '--method', default='GET', choices=['GET', 'POST', 'PUT', 'DELETE'], help='🔨 HTTP method')
    parser.add_argument('--data', help='📤 JSON data for POST/PUT requests')
    
    args = parser.parse_args()
    
    data = None
    if args.data:
        import json
        try:
            data = json.loads(args.data)
        except json.JSONDecodeError:
            console.print("💥 Error: Invalid JSON data", style="bold red")
            return
    
    tester = LoadTester()
    asyncio.run(tester.run_load_test(args.url, args.requests, args.concurrent, args.method, data))

if __name__ == "__main__":
    main()