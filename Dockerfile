# Emulate AWS Lambda runtime
FROM public.ecr.aws/lambda/python:3.10

# Copy requirements and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the application code
COPY . ${LAMBDA_TASK_ROOT}

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV PYTHONPATH=${LAMBDA_TASK_ROOT}

# Add Lambda specific dependencies
RUN pip install awslambdaric mangum

# Create a script to run the Lambda handler
COPY <<EOF ${LAMBDA_TASK_ROOT}/lambda.py
from mangum import Mangum
from app import create_app

app = create_app()
handler = Mangum(app)
EOF

# Set the handler
CMD [ "lambda.handler" ]

EXPOSE 5000