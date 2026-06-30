import argparse
import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()
import httpx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

APP_NAME = "AI Research Agent"


def ensure_environment():
    required_vars = ["OLLAMA_BASE_URL", "OLLAMA_MODEL", "SERPER_API_KEY"]
    missing = [name for name in required_vars if not os.getenv(name)]
    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}. "
            "Please add them to your .env file (see README)."
        )

    # Normalize env into runtime variables
    os.environ["OLLAMA_BASE_URL"] = os.getenv("OLLAMA_BASE_URL")
    os.environ["OLLAMA_MODEL"] = os.getenv("OLLAMA_MODEL")

    # Quick Ollama health check
    try:
        check_ollama_server(os.environ["OLLAMA_BASE_URL"], os.environ["OLLAMA_MODEL"])
    except RuntimeError:
        raise


def check_ollama_server(base_url: str, model: str):
    """Validate the Ollama server is reachable and the model is available.

    Tries a few common endpoints and raises RuntimeError with a clear message
    if the server or model is not available.
    """
    if not base_url:
        raise RuntimeError("OLLAMA_BASE_URL is empty")

    # Normalize base_url (no trailing slash)
    base_url = base_url.rstrip('/')

    endpoints = [
        f"{base_url}/models",
        f"{base_url}/api/models",
        f"{base_url}/v1/models",
    ]

    last_err = None
    for ep in endpoints:
        try:
            resp = httpx.get(ep, timeout=5.0)
        except Exception as e:
            last_err = e
            continue

        if resp.status_code == 200:
            try:
                data = resp.json()
            except Exception:
                # If not JSON, assume server responded but can't parse
                return True

            # data may be a list of model dicts or a dict
            model_names = []
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        # common keys: name, model, id
                        for key in ('name', 'model', 'id'):
                            if key in item and isinstance(item[key], str):
                                model_names.append(item[key])
                    elif isinstance(item, str):
                        model_names.append(item)
            elif isinstance(data, dict):
                # try common wrapper keys
                if 'models' in data and isinstance(data['models'], list):
                    for item in data['models']:
                        if isinstance(item, dict):
                            for key in ('name', 'model', 'id'):
                                if key in item and isinstance(item[key], str):
                                    model_names.append(item[key])
                if 'data' in data and isinstance(data['data'], list):
                    for item in data['data']:
                        if isinstance(item, dict):
                            for key in ('id', 'name', 'model'):
                                if key in item and isinstance(item[key], str):
                                    model_names.append(item[key])

            # Accept both 'qwen2.5:3b' and 'ollama/qwen2.5:3b'
            wanted = model
            if wanted.startswith('ollama/'):
                wanted_variants = [wanted, wanted.split('/', 1)[1]]
            else:
                wanted_variants = [wanted, f"ollama/{wanted}"]

            for v in wanted_variants:
                if v in model_names:
                    return True

            # If server OK but model not found, raise with instructions
            raise RuntimeError(
                f"Ollama server reachable at {base_url} but model '{model}' not found.\n"
                "Run: ollama pull {model}  OR  ollama serve and then ollama pull {model}\n"
                "Example: ollama pull qwen2.5:3b"
            )

    # If none of the endpoints worked, raise a connection error
    raise RuntimeError(
        f"Could not reach Ollama server at {base_url}. "
        "Make sure the server is running with: ollama serve"
    )

from crew import research_crew


def main():
    parser = argparse.ArgumentParser(
        description="Run the Ollama-powered AI research workflow"
    )

    parser.add_argument(
        "--topic",
        required=True,
        help="Research topic to investigate"
    )

    args = parser.parse_args()

    try:
        ensure_environment()

        logger.info("Starting %s", APP_NAME)
        print("\n====================================")
        print(f"🚀 Starting {APP_NAME}")
        print("====================================\n")

        result = research_crew.kickoff(inputs={"topic": args.topic})

        logger.info("Research completed successfully")
        print("\n====================================")
        print("✅ Research Completed")
        print("====================================\n")
        print(result)

    except RuntimeError as runtime_error:
        logger.error(runtime_error)
        sys.exit(1)
    except Exception:
        logger.exception("An unexpected error occurred while running the project.")
        sys.exit(1)


if __name__ == "__main__":
    main()