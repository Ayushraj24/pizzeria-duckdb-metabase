FROM eclipse-temurin:21-jre

ARG METABASE_VERSION=0.59.8
ARG DUCKDB_DRIVER_URL=https://github.com/motherduckdb/metabase_duckdb_driver/releases/latest/download/duckdb.metabase-driver.jar

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L "https://downloads.metabase.com/v${METABASE_VERSION}/metabase.jar" -o /app/metabase.jar
RUN mkdir -p /app/plugins \
    && curl -L "${DUCKDB_DRIVER_URL}" -o /app/plugins/duckdb.metabase-driver.jar

ENV MB_PLUGINS_DIR=/app/plugins
ENV MB_DB_FILE=/metabase-data/metabase.db

EXPOSE 3000

CMD ["java", "-jar", "/app/metabase.jar"]

