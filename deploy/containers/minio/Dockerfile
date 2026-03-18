FROM minio/minio:RELEASE.2025-09-07T16-13-09Z-cpuv1

EXPOSE 9000
EXPOSE 9001

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]

CMD ["server", "/data", "--console-address", ":9001"]
