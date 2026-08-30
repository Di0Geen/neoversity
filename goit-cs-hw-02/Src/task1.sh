#!/bin/bash

# Список вебсайтів для перевірки
websites=(
    "https://google.com"
    "https://facebook.com"
    "https://twitter.com"
)

# Файл для збереження результатів
log_file="website_status.log"

# Очищення старого вмісту лог-файлу
> "$log_file"

# Перевірка кожного вебсайту
for website in "${websites[@]}"; do
    status_code=$(curl -L -s -o /dev/null -w "%{http_code}" "$website")

    if [ "$status_code" -eq 200 ]; then
        echo "$website is UP" >> "$log_file"
    else
        echo "$website is DOWN" >> "$log_file"
    fi
done

echo "Results have been written to $log_file"