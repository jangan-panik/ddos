# 🔥💀 SEOWOT48 Ultimate Load Tester 💀🔥

Ultimate collection of high-performance load testing tools for stress testing servers and APIs.

## 🚀 Features

### 📊 Basic Load Tester (`load_test.py`)
- Simple concurrent request testing
- Customizable request count and concurrency
- Multiple HTTP methods support
- Real-time progress tracking
- Detailed performance reports

### 🇮🇩 Indonesian Interface (`load_test_indo.py`)
- Complete Indonesian language interface
- Interactive configuration input
- User-friendly prompts
- Colorful output with emojis
- Repeat testing without restart

### ⚔️ Continuous Destroyer (`load_test_continuous.py`)
- **Continuous attack until server down**
- Wave-based assault system
- Auto-detection of server failure
- Customizable error thresholds
- Real-time wave monitoring

### 💀 Ultimate Destroyer (`seowot48_ultimate.py`)
- **MAXIMUM DEVASTATION MODE**
- Multi-target attack support
- 5 intensity levels (up to 50,000 req/wave)
- Advanced features:
  - Request flooding
  - Random payload generation
  - Random User-Agents
  - IP spoofing headers
  - Mixed HTTP methods
- Real-time dashboard
- Smart server down detection

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/yourusername/seowot48-load-tester.git
cd seowot48-load-tester

# Install dependencies
pip install -r requirements.txt
```

## 🎯 Usage

### Basic Load Test
```bash
python load_test.py https://httpbin.org/get -n 1000 -c 50
```

### Indonesian Interactive Mode
```bash
python load_test_indo.py
```

### Continuous Attack Mode
```bash
python load_test_continuous.py
```

### Ultimate Destroyer Mode
```bash
python seowot48_ultimate.py
```

## ⚡ Intensity Levels

| Level | Requests/Wave | Concurrent | Description |
|-------|---------------|------------|-------------|
| 1 | 1,000 | 50 | Ringan |
| 2 | 5,000 | 100 | Sedang |
| 3 | 10,000 | 200 | Berat |
| 4 | 25,000 | 500 | BRUTAL |
| 5 | 50,000 | 1,000 | APOCALYPSE 💀 |

## 🎯 Target Format Support

- **HTTP/HTTPS URLs**: `http://example.com`, `https://api.example.com`
- **IP Addresses**: `http://192.168.1.100`, `https://10.0.0.5:8080`
- **Localhost**: `http://localhost:3000`, `http://127.0.0.1:8000`
- **Custom Ports**: `http://server.com:8080`, `https://api.com:443`

## 📈 Features Comparison

| Feature | Basic | Indonesian | Continuous | Ultimate |
|---------|-------|------------|------------|----------|
| Single Target | ✅ | ✅ | ✅ | ✅ |
| Multiple Targets | ❌ | ❌ | ❌ | ✅ |
| Indonesian UI | ❌ | ✅ | ✅ | ❌ |
| Continuous Attack | ❌ | ❌ | ✅ | ✅ |
| Random Payloads | ❌ | ❌ | ❌ | ✅ |
| IP Spoofing | ❌ | ❌ | ❌ | ✅ |
| Max Concurrent | 100 | 100 | 100 | 1,000 |
| Max Requests/Wave | 1,000 | 1,000 | 500 | 50,000 |

## 🔧 Configuration Examples

### Basic Test
```bash
python load_test.py http://192.168.1.100:8080 -n 5000 -c 100 -m POST --data '{"test": "data"}'
```

### Ultimate Multi-Target
```
Targets: 
- http://192.168.1.100
- http://10.0.0.5:8080  
- https://api.example.com

Intensity: APOCALYPSE (50,000 req/wave)
Concurrent: 1,000 users
Features: All enabled
```

## 🚨 Ethical Usage

⚠️ **WARNING**: This tool is designed for:
- Testing your own servers
- Load testing with permission
- Performance benchmarking
- Educational purposes

🚫 **DO NOT USE FOR**:
- Attacking servers you don't own
- DDoS attacks
- Illegal activities
- Malicious purposes

## 📊 Sample Output

```
🔥💀 SEOWOT48 ULTIMATE LIVE DASHBOARD 💀🔥
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ Metric             ┃        Value ┃ Status             ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ ⚔️ Wave Number      │           #5 │ 💀 ANNIHILATION    │
│ ⏱️ Attack Duration  │       45.2s │ 🕐                 │
│ 🚀 Requests Fired  │       50,000 │ 💥                 │
│ 💥 Requests/Second  │      1,106.2 │ ⚡                 │
│ ✅ Successful Hits  │       48,234 │ 💚                 │
│ ❌ Failed Attacks   │        1,766 │ 💔                 │
│ 📊 Error Rate       │        3.5% │ ⚠️                 │
│ ⚡ Avg Response     │         84ms │ 📈                 │
│ 📦 Data Transferred │      125.4MB │ 📊                 │
│ 🎯 Server Status    │ 🛡️ DEFENDING │ 🔥                 │
└────────────────────┴──────────────┴────────────────────┘
```

## 🛠️ Requirements

- Python 3.7+
- aiohttp
- rich

## 📄 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch  
5. Create Pull Request

## ⭐ Support

If you find this tool useful, please give it a ⭐ on GitHub!

---

**Made with 💀 by SEOWOT48**