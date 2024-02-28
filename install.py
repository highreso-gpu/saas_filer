import launch

if not launch.is_installed("python-dotenv"):
    launch.run_pip("install python-dotenv", desc='python-dotenv')
    print("=========================")
    print("python-dotenv installed")
    print("=========================")

if not launch.is_installed("Flask"):
    launch.run_pip("install Flask", desc='Flask')
    print("=========================")
    print("Flask installed")
    print("=========================")

if not launch.is_installed("flask-cors"):
    launch.run_pip("install flask-cors", desc='flask-cors')
    print("=========================")
    print("flask-cors installed")
    print("=========================")

