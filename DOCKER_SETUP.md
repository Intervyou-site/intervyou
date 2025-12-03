# 🐳 Docker Setup for AI-Powered IDE

## Quick Setup

### Pull All Required Images

```powershell
# Python (for Python code execution)
docker pull python:3.11-slim

# Node.js (for JavaScript code execution)
docker pull node:20-slim

# Java (for Java code execution)
docker pull eclipse-temurin:17-jdk-alpine

# GCC (for C/C++ code execution)
docker pull gcc:11
```

## Verify Installation

```powershell
# Check all images are downloaded
docker images

# Should see:
# python:3.11-slim
# node:20-slim
# eclipse-temurin:17-jdk-alpine
# gcc:11
```

## Image Details

| Language | Image | Size | Purpose |
|----------|-------|------|---------|
| Python | `python:3.11-slim` | ~120MB | Python 3.11 runtime |
| JavaScript | `node:20-slim` | ~180MB | Node.js 20 runtime |
| Java | `eclipse-temurin:17-jdk-alpine` | ~330MB | Java 17 JDK |
| C/C++ | `gcc:11` | ~1.2GB | GCC 11 compiler |

## Why These Images?

### Python: `python:3.11-slim`
- ✅ Latest stable Python
- ✅ Small size (slim variant)
- ✅ Includes pip
- ✅ Debian-based

### JavaScript: `node:20-slim`
- ✅ Latest LTS Node.js
- ✅ Small size (slim variant)
- ✅ Includes npm
- ✅ Debian-based

### Java: `eclipse-temurin:17-jdk-alpine`
- ✅ OpenJDK replacement (official)
- ✅ Java 17 LTS
- ✅ Alpine-based (smaller)
- ✅ Maintained by Eclipse Foundation

### C/C++: `gcc:11`
- ✅ Latest GCC compiler
- ✅ Supports C++20
- ✅ Includes g++ and gcc
- ✅ Full toolchain

## Testing Images

### Test Python
```powershell
docker run --rm python:3.11-slim python -c "print('Hello from Python!')"
```

### Test Node.js
```powershell
docker run --rm node:20-slim node -e "console.log('Hello from Node!')"
```

### Test Java
```powershell
docker run --rm eclipse-temurin:17-jdk-alpine java -version
```

### Test GCC
```powershell
docker run --rm gcc:11 gcc --version
```

## Troubleshooting

### Issue: Image Pull Failed
**Solution:**
```powershell
# Check Docker is running
docker --version

# Check internet connection
ping docker.io

# Try pulling again
docker pull <image-name>
```

### Issue: Disk Space
**Solution:**
```powershell
# Check disk space
docker system df

# Clean up unused images
docker system prune -a
```

### Issue: Slow Pull
**Solution:**
- Use a faster internet connection
- Images are cached after first pull
- Consider using a Docker registry mirror

## Without Docker

If you can't use Docker, the IDE will automatically fall back to local execution using:
- System Python
- System Node.js
- System Java
- System GCC

Make sure these are installed locally:
```powershell
python --version
node --version
java --version
gcc --version
```

## Security Benefits of Docker

1. **Isolation**: Code runs in containers, not on host
2. **No Network**: Containers have no internet access
3. **Resource Limits**: Memory and CPU limits enforced
4. **Clean State**: Each execution starts fresh
5. **No Persistence**: Containers are destroyed after use

## Performance Tips

1. **Pre-pull Images**: Pull all images before first use
2. **Keep Images Updated**: Regularly update for security
3. **Use Slim Variants**: Smaller images = faster startup
4. **Local Cache**: Docker caches images locally

## Updating Images

```powershell
# Update all images
docker pull python:3.11-slim
docker pull node:20-slim
docker pull eclipse-temurin:17-jdk-alpine
docker pull gcc:11

# Remove old versions
docker image prune
```

## Alternative Images

If you need different versions:

### Python
```powershell
docker pull python:3.10-slim  # Python 3.10
docker pull python:3.12-slim  # Python 3.12
```

### Node.js
```powershell
docker pull node:18-slim  # Node.js 18 LTS
docker pull node:21-slim  # Node.js 21
```

### Java
```powershell
docker pull eclipse-temurin:11-jdk-alpine  # Java 11
docker pull eclipse-temurin:21-jdk-alpine  # Java 21
```

### GCC
```powershell
docker pull gcc:10  # GCC 10
docker pull gcc:12  # GCC 12
```

## Docker Compose (Optional)

Create `docker-compose.yml` for easier management:

```yaml
version: '3.8'
services:
  python:
    image: python:3.11-slim
    command: tail -f /dev/null
  
  node:
    image: node:20-slim
    command: tail -f /dev/null
  
  java:
    image: eclipse-temurin:17-jdk-alpine
    command: tail -f /dev/null
  
  gcc:
    image: gcc:11
    command: tail -f /dev/null
```

## Summary

✅ **All images pulled successfully!**

Your IDE can now execute code in:
- 🐍 Python 3.11
- 🟢 JavaScript (Node 20)
- ☕ Java 17
- ⚙️ C/C++ (GCC 11)

All in secure, isolated Docker containers!

---

**Ready to code safely! 🚀**
