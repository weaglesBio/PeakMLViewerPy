import UI.MainView
import Data.DataAccess

def main():

    #Initialize data object
    data = Data.DataAccess.PeakMLData()

    #Creates main window
    UI.MainView.MainView(data)

if __name__ == "__main__":
    main()
