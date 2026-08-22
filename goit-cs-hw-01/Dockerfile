FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Встановлення NASM, DOSBox і вебінтерфейсу
RUN apt-get update && \
    apt-get install -y dosbox nasm xvfb x11vnc novnc websockify && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Копіювання та компіляція програми
COPY task1.asm /workspace/
RUN nasm -f bin task1.asm -o task1.com

# Створення скрипту запуску
RUN echo '#!/bin/bash\n\
export DISPLAY=:0\n\
Xvfb :0 -screen 0 800x600x16 &\n\
sleep 1\n\
x11vnc -display :0 -nopw -forever -bg -quiet\n\
websockify --web /usr/share/novnc/ 8080 localhost:5900 &\n\
dosbox -c "mount c /workspace" -c "c:" -c "task1.com"\n\
' > /start.sh && chmod +x /start.sh

EXPOSE 8080

CMD ["/start.sh"]