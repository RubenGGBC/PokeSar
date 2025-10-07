# Guía de instalación y verificación del entorno

Este documento explica cómo preparar tu entorno para ejecutar este proyecto, incluyendo la instalación de **.NET 8.0**, la creación de un entorno virtual de **Python**, y cómo verificar que todo está correctamente configurado.

---

## 🧩 1. Instalación de .NET 8.0

### 🔹 Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y dotnet-sdk-8.0
```

> Si tu distribución no tiene el paquete disponible, puedes usar los paquetes oficiales de Microsoft:
> [https://learn.microsoft.com/dotnet/core/install/linux](https://learn.microsoft.com/dotnet/core/install/linux)

### 🔹 macOS

Usando Homebrew:

```bash
brew install --cask dotnet
```

O desde el instalador oficial:
[https://dotnet.microsoft.com/en-us/download/dotnet/8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

### 🔹 Windows

1. Descarga el instalador desde  
   👉 [https://dotnet.microsoft.com/en-us/download/dotnet/8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)
2. Ejecuta el instalador y sigue las instrucciones.
3. Verifica la instalación con:

```powershell
dotnet --version
```

Debe mostrar algo como:
```
8.0.xxx
```

---

## 🐍 2. Crear entorno virtual e instalar dependencias

Asegúrate de tener Python 3.10+ instalado.  
Verifica con:

```bash
python3 --version
```

### Crear el entorno virtual

```bash
python3 -m venv venv
```

### Activar el entorno virtual

- **Linux / macOS**
  ```bash
  source venv/bin/activate
  ```

- **Windows (PowerShell)**
  ```powershell
  venv\Scripts\Activate.ps1
  ```

### Instalar dependencias

Con el entorno activado, instala los requisitos:

```bash
pip install -r requirements.txt
```

---

## ✅ 3. Verificación del entorno

### Verificar .NET

```bash
dotnet --info
```

Deberías ver información del SDK 8.0.

### Verificar Python y dependencias

```bash
python --version
pip list
```

Asegúrate de que se muestran las dependencias del `requirements.txt`.

### (Opcional) Verificar ejecución del proyecto

Si el proyecto incluye un archivo principal (por ejemplo, `main.py` o `Program.cs`), ejecútalo:

- **Python:**
  ```bash
  python main.py
  ```

- **.NET:**
  ```bash
  dotnet run
  ```

Si no aparecen errores, el entorno está correctamente configurado 🎉

---

## 🧠 Consejos

- Si usas VS Code, asegúrate de seleccionar el intérprete Python correcto (`venv`).
- En Linux, puede que necesites agregar permisos de ejecución:
  ```bash
  chmod +x venv/bin/activate
  ```
