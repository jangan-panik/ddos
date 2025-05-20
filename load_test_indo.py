import asyncio
import aiohttp
import time
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
from rich.prompt import Prompt, IntPrompt, Confirm

console = Console()

@dataclass
class HasilTes:
    kode_status: int
    waktu_respon: float
    error: str = None

class TesterBeban:
    def __init__(self):
        self.hasil = []
        self.waktu_mulai = None
        self.console = Console()
        
    def tampilkan_banner(self):
        banner = """
 ███████ ███████  ██████  ██     ██  ██████  ████████ ██   ██  █████  
 ██      ██      ██    ██ ██     ██ ██    ██    ██    ██   ██ ██   ██ 
 ███████ █████   ██    ██ ██  █  ██ ██    ██    ██    ███████  █████  
      ██ ██      ██    ██ ██ ███ ██ ██    ██    ██         ██ ██   ██ 
 ███████ ███████  ██████   ███ ███   ██████     ██         ██  █████  
                                                                      
         ⚡ PENGHANCUR SERVER INDONESIA ⚡                           
        """
        
        self.console.print(Panel(
            Align.center(Text(banner, style="bold cyan")),
            title="🇮🇩 SEOWOT48 LOAD TESTER INDONESIA 🇮🇩",
            border_style="bright_red",
            box=box.DOUBLE
        ))
    
    def input_konfigurasi(self):
        self.console.print("\n🎯 [bold green]Masukkan konfigurasi test:[/bold green]\n")
        
        # Input URL
        url = Prompt.ask("🌐 [bold blue]URL target yang akan dibom[/bold blue]", 
                        default="https://httpbin.org/get")
        
        # Input jumlah request
        jumlah_request = IntPrompt.ask("📊 [bold yellow]Berapa jumlah request total?[/bold yellow]", 
                                     default=1000, show_default=True)
        
        # Input concurrent users
        pengguna_bersamaan = IntPrompt.ask("👥 [bold cyan]Berapa pengguna bersamaan?[/bold cyan]", 
                                         default=50, show_default=True)
        
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
        
        return url, jumlah_request, pengguna_bersamaan, method, data
    
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

    def tampilkan_konfigurasi_tes(self, url: str, jumlah_request: int, pengguna_bersamaan: int, method: str):
        tabel_config = Table(title="🚀 Konfigurasi Serangan", box=box.ROUNDED, border_style="bright_yellow")
        tabel_config.add_column("Parameter", style="bold white", justify="left")
        tabel_config.add_column("Nilai", style="bright_green", justify="left")
        
        tabel_config.add_row("🎯 URL Target", url)
        tabel_config.add_row("📊 Total Request", f"{jumlah_request:,}")
        tabel_config.add_row("👥 Pengguna Bersamaan", f"{pengguna_bersamaan}")
        tabel_config.add_row("🔨 Metode HTTP", method)
        tabel_config.add_row("⚡ Mesin", "SEOWOT48 AsyncIO Indonesia")
        
        self.console.print(tabel_config)
        
    def buat_progress_bar(self, total_request: int):
        return Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=60, style="bright_red", complete_style="bright_green"),
            MofNCompleteColumn(),
            TextColumn("[bold green]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console
        )

    async def jalankan_tes_beban(self, url: str, jumlah_request: int, pengguna_bersamaan: int, method: str = 'GET', data: dict = None):
        self.tampilkan_konfigurasi_tes(url, jumlah_request, pengguna_bersamaan, method)
        
        self.console.print("\n⚠️ [bold red]PERINGATAN: Serangan akan dimulai dalam 3 detik...[/bold red]")
        for i in range(3, 0, -1):
            self.console.print(f"⏰ {i}...", end=" ")
            await asyncio.sleep(1)
        self.console.print("🚀 [bold green]MULAI SERANGAN![/bold green]\n")
        
        connector = aiohttp.TCPConnector(limit=pengguna_bersamaan * 2, limit_per_host=pengguna_bersamaan)
        timeout = aiohttp.ClientTimeout(total=60)
        
        with self.buat_progress_bar(jumlah_request) as progress:
            task = progress.add_task("💥 Menghancurkan server...", total=jumlah_request)
            
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                self.waktu_mulai = time.time()
                
                semaphore = asyncio.Semaphore(pengguna_bersamaan)
                
                async def request_terbatas():
                    async with semaphore:
                        hasil = await self.kirim_request(session, url, method, data)
                        self.hasil.append(hasil)
                        progress.advance(task)
                        return hasil
                
                tasks = [request_terbatas() for _ in range(jumlah_request)]
                await asyncio.gather(*tasks)
        
        self.tampilkan_laporan_akhir()

    def tampilkan_laporan_akhir(self):
        waktu_total = time.time() - self.waktu_mulai
        
        hasil_sukses = [r for r in self.hasil if r.kode_status == 200]
        hasil_error = [r for r in self.hasil if r.kode_status != 200]
        
        waktu_respon = [r.waktu_respon for r in hasil_sukses] if hasil_sukses else [0]
        
        self.console.print("\n")
        
        tabel_ringkasan = Table(title="⚡ LAPORAN KINERJA SEOWOT48", box=box.DOUBLE_EDGE, border_style="bright_magenta")
        tabel_ringkasan.add_column("Metrik", style="bold white", justify="left")
        tabel_ringkasan.add_column("Nilai", style="bright_green", justify="right")
        tabel_ringkasan.add_column("Status", style="bold yellow", justify="center")
        
        rps = len(self.hasil) / waktu_total
        tingkat_sukses = (len(hasil_sukses) / len(self.hasil)) * 100 if self.hasil else 0
        
        tabel_ringkasan.add_row("🕐 Waktu Total", f"{waktu_total:.2f} detik", "✅")
        tabel_ringkasan.add_row("🚀 Request/Detik", f"{rps:.2f}", "⚡" if rps > 100 else "🔥")
        tabel_ringkasan.add_row("✅ Request Berhasil", f"{len(hasil_sukses):,}", "💚")
        tabel_ringkasan.add_row("❌ Request Gagal", f"{len(hasil_error):,}", "💔" if hasil_error else "✨")
        tabel_ringkasan.add_row("📈 Tingkat Keberhasilan", f"{tingkat_sukses:.1f}%", "🎯" if tingkat_sukses > 95 else "⚠️")
        
        if waktu_respon:
            tabel_ringkasan.add_row("⚡ Respon Tercepat", f"{min(waktu_respon)*1000:.0f}ms", "🏃‍♂️")
            tabel_ringkasan.add_row("📊 Respon Rata-rata", f"{statistics.mean(waktu_respon)*1000:.0f}ms", "📈")
            tabel_ringkasan.add_row("🐌 Respon Terlambat", f"{max(waktu_respon)*1000:.0f}ms", "🐢")
            if len(waktu_respon) >= 20:
                tabel_ringkasan.add_row("📐 Persentil ke-95", f"{statistics.quantiles(waktu_respon, n=20)[18]*1000:.0f}ms", "📏")
        
        self.console.print(tabel_ringkasan)
        
        if hasil_error:
            self.tampilkan_rincian_error(hasil_error)
        
        self.tampilkan_vonis_kinerja(tingkat_sukses, rps, statistics.mean(waktu_respon) if waktu_respon else 0)

    def tampilkan_rincian_error(self, hasil_error):
        tabel_error = Table(title="💥 Rincian Error", box=box.ROUNDED, border_style="red")
        tabel_error.add_column("Kode Status", style="bold red")
        tabel_error.add_column("Jumlah", style="bright_red", justify="right")
        tabel_error.add_column("Persentase", style="yellow", justify="right")
        
        hitung_error = {}
        for hasil in hasil_error:
            kode = hasil.kode_status if hasil.kode_status != 0 else "Error Koneksi"
            hitung_error[kode] = hitung_error.get(kode, 0) + 1
        
        total_error = len(hasil_error)
        for kode, jumlah in sorted(hitung_error.items()):
            persentase = (jumlah / total_error) * 100
            tabel_error.add_row(str(kode), f"{jumlah:,}", f"{persentase:.1f}%")
        
        self.console.print(tabel_error)

    def tampilkan_vonis_kinerja(self, tingkat_sukses, rps, rata_waktu_respon):
        if tingkat_sukses >= 99 and rps >= 1000 and rata_waktu_respon < 0.1:
            vonis = "🔥 PERFORMA LEGENDARIS! Server ANTI PELURU! 🔥"
            style = "bold green on black"
        elif tingkat_sukses >= 95 and rps >= 500:
            vonis = "⚡ LUAR BIASA! Server menangani beban seperti RAJA! ⚡"
            style = "bold bright_green"
        elif tingkat_sukses >= 90 and rps >= 100:
            vonis = "👍 BAGUS! Server kuat menghadapi tekanan! 👍"
            style = "bold yellow"
        elif tingkat_sukses >= 80:
            vonis = "⚠️ LUMAYAN! Server berjuang tapi bertahan! ⚠️"
            style = "bold bright_yellow"
        else:
            vonis = "💥 KRITIS! Server sedang DIHANCURKAN! 💥"
            style = "bold red"
        
        self.console.print("\n")
        self.console.print(Panel(
            Align.center(Text(vonis, style=style)),
            title="🎯 VONIS SEOWOT48",
            border_style="bright_cyan",
            box=box.DOUBLE
        ))

def main():
    tester = TesterBeban()
    
    while True:
        try:
            tester.tampilkan_banner()
            
            url, jumlah_request, pengguna_bersamaan, method, data = tester.input_konfigurasi()
            
            asyncio.run(tester.jalankan_tes_beban(url, jumlah_request, pengguna_bersamaan, method, data))
            
            console.print("\n")
            ulang = Confirm.ask("🔄 [bold blue]Mau tes lagi?[/bold blue]", default=True)
            if not ulang:
                console.print("👋 [bold green]Terima kasih telah menggunakan SEOWOT48![/bold green]")
                break
            else:
                console.clear()
                
        except KeyboardInterrupt:
            console.print("\n❌ [bold red]Tes dibatalkan oleh pengguna![/bold red]")
            break
        except Exception as e:
            console.print(f"\n💥 [bold red]Terjadi error: {e}[/bold red]")
            ulang = Confirm.ask("🔄 Coba lagi?", default=True)
            if not ulang:
                break

if __name__ == "__main__":
    main()