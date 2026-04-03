"""Allow running ``python -m zohopy`` to launch the setup wizard."""

from zohopy.setup import interactive_setup

if __name__ == "__main__":
    interactive_setup()
