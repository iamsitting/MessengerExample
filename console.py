from app import App

if __name__ == "__main__":
    import sys
#    for a in sys.argv:
#        print a
#    print len(sys.argv)
    if len(sys.argv) < 2:
        print 'usage: python console.py run'
        sys.exit(1)
    else:
        if sys.argv[1] == 'run':
            app = App()
            app.run()
        elif sys.argv[1] == '-x'\
        and sys.argv[2] == 'run':
            app = App(gui=False)
            app.run()
        else:
            print 'usage: python console.py [-x] run'
            sys.exit(1)
#    app = App()
#    app.run()
