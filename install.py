import launch

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
