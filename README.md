# Discord-RPC---Terminal-Kitty

Discord RPC para Terminal Kitty - Guia de Instalação

## 📋 Requisitos

- Arch Linux
- Terminal Kitty
- Python 3
- Discord instalado e rodando

## 🚀 Instalação

### 1. Instalar dependências Python

```bash
# Instalar pip se necessário
sudo pacman -S python-pip

# Instalar as bibliotecas necessárias
pip install pypresence psutil --break-system-packages
```

### 2. Criar aplicação no Discord

1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique em **"New Application"**
3. Dê um nome (ex: "Kitty Terminal")
4. Copie o **Application ID** (você vai precisar dele)

### 3. (Opcional) Adicionar ícone personalizado

1. No Discord Developer Portal, vá em **Rich Presence > Art Assets**
2. Faça upload de uma imagem com o nome **"terminal"**
3. Isso será exibido como ícone no seu status

### 4. Configurar o script

1. Abra o arquivo `kitty_discord_rpc.py`
2. Encontre a linha:
```python
CLIENT_ID = "YOUR_CLIENT_ID_HERE"
```
3. Substitua por seu Application ID:
```python
CLIENT_ID = "1234567890123456789"  # Seu ID aqui
```

### 5. Tornar o script executável

```bash
chmod +x kitty_discord_rpc.py
```

## 🎮 Uso

### Executar manualmente

```bash
python kitty_discord_rpc.py
```

ou

```bash
./kitty_discord_rpc.py
```

### Executar automaticamente no boot

#### Opção 1: Usando systemd (recomendado)

Crie o arquivo de serviço:

```bash
mkdir -p ~/.config/systemd/user/
nano ~/.config/systemd/user/kitty-discord-rpc.service
```

Cole o seguinte conteúdo:

```ini
[Unit]
Description=Kitty Discord RPC
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python /caminho/completo/para/kitty_discord_rpc.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

**Importante:** Substitua `/caminho/completo/para/` pelo caminho real do script!

Ative e inicie o serviço:

```bash
systemctl --user enable kitty-discord-rpc.service
systemctl --user start kitty-discord-rpc.service
```

Verificar status:

```bash
systemctl --user status kitty-discord-rpc.service
```

#### Opção 2: Adicionar ao autostart do seu WM/DE

**Para i3/sway:**
Adicione ao `~/.config/i3/config` ou `~/.config/sway/config`:
```
exec --no-startup-id python /caminho/para/kitty_discord_rpc.py
```

**Para Hyprland:**
Adicione ao `~/.config/hyprland/hyprland.conf`:
```
exec-once = python /caminho/para/kitty_discord_rpc.py
```

**Para GNOME/KDE:**
Use o aplicativo de "Startup Applications" e adicione o comando.

## 🎨 Personalização

### Modificar frequência de atualização

No script, encontre:
```python
time.sleep(5)  # Atualiza a cada 5 segundos
```

Altere o valor para ajustar a frequência.

### Adicionar mais informações

Você pode modificar a função `update_presence()` para mostrar:
- Nome do diretório atual
- Uso de CPU/RAM
- Tempo de uptime
- E muito mais!

## 🔧 Solução de Problemas

### "Erro ao conectar"
- Verifique se o Discord está rodando
- Reinicie o Discord
- Verifique se o Application ID está correto

### "No module named 'pypresence'"
```bash
pip install pypresence psutil --break-system-packages
```

### Script não detecta processos
- Verifique se você está usando o Kitty
- Alguns processos podem não ser detectados por questões de permissão

### Parar o serviço systemd
```bash
systemctl --user stop kitty-discord-rpc.service
systemctl --user disable kitty-discord-rpc.service
```

## 📝 O que é exibido

- **Quando há comando rodando:** Mostra o nome do programa e comando
- **Quando está idle:** Mostra apenas o terminal e shell
- **Tempo:** Quanto tempo o RPC está ativo

## 🎯 Exemplo de exibição

```
🎮 Jogando Kitty Terminal
Rodando: nvim
Terminal: Kitty
⏱️ 00:15:32 decorridos
```

## 🤝 Melhorias futuras

Sinta-se livre para modificar o script! Algumas ideias:
- Ignorar comandos específicos
- Mostrar apenas comandos de desenvolvimento
- Integração com Git (mostrar branch atual)
- Suporte para múltiplas janelas Kitty

## 📄 Licença

Use livremente! 🚀
