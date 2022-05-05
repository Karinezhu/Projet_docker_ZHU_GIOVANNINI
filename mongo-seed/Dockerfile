FROM mongo

COPY Dry_Bean_Dataset.csv /Dry_Bean_Dataset.csv


ADD import.sh /import.sh
RUN chmod +x /import.sh

CMD ["/bash","/import.sh"]

