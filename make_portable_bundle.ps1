# Makes a portable bundle from Book Keeper.
# Prerequisits: pyinstaller, 7Zip4PowerShell.

$bundle_folder = ".\dist\book_keeper_window\"

pyinstaller --icon=".\assets\icons\icons8-audio-book-50.ico" .\book_keeper_window.pyw

if ($?)
{
    try
    {
        Expand-7Zip .\ffmpeg.7z $bundle_folder
    }
    catch
    {
        Write-Output $_
        Exit
    }

    Copy-Item -r .\assets $bundle_folder
}
