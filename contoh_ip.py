# Contoh target dengan IP server

targets_contoh = [
    # Server lokal
    "http://127.0.0.1:8000",
    "http://localhost:3000", 
    
    # Server dalam jaringan lokal
    "http://192.168.1.100",
    "http://192.168.1.50:8080",
    "http://10.0.0.5:9000",
    
    # Server publik dengan IP
    "http://8.8.8.8",  # Google DNS (hanya untuk test)
    "https://1.1.1.1", # Cloudflare DNS
    
    # Server dengan port khusus
    "http://172.16.0.10:1337",
    "https://203.194.112.20:8443",
    
    # API endpoints dengan IP
    "http://192.168.1.100/api/users",
    "http://10.0.0.5:3000/health",
]

print("🎯 Contoh target IP yang bisa diserang:")
for i, target in enumerate(targets_contoh, 1):
    print(f"{i:2d}. {target}")