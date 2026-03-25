FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y curl wget wireguard-tools
RUN wget https://github.com/ViRb3/wgcf/releases/download/v2.2.22/wgcf_2.2.22_linux_amd64 -O /usr/local/bin/wgcf
RUN chmod +x /usr/local/bin/wgcf

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# Port Listen လုပ်စရာမလိုတဲ့အတွက် CMD ပဲ တိုက်ရိုက် run ပါမယ်
CMD ["python", "bot.py"]
