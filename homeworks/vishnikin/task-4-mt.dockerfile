FROM python:3.11-slim AS builder

WORKDIR /apps/first-app

COPY ../../apps/course-app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt  

COPY ../../apps/course-app/src ./src

RUN useradd appuser

FROM python:3.11-slim
#add copying of site-packages from builder stage as without these files the application won't work and container fails to start
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /apps/first-app /apps/first-app
WORKDIR /apps/first-app
#add copying of /etc/passwd to have appuser in final image
COPY --from=builder /etc/passwd /etc/passwd 

EXPOSE 8080

USER appuser

#start the application with python3 as just python may not be available in slim images
CMD ["python3", "src/main.py", "--host", "0.0.0.0", "--port", "8080"]



 