#NoEnv
SendMode, Input
SetBatchLines, -1
SetTitleMatchMode, 2

; ------------------------------------------------
; 1) Configuration
; ------------------------------------------------
GameTitle := "AQ: First Contact"   ; Partial or exact title of your game window

; Coordinates for the "health text" region (where red text appears)
; These are relative to the window *client* area (if using CoordMode, Pixel, Window).
healthX1 := 1111
healthY1 := 390
healthX2 := 1140
healthY2 := 490

; Coordinates for the bottom-left button region (to check if it's "solid")
buttonX1 := 525
buttonY1 := 750
buttonX2 := 565
buttonY2 := 790

; The coordinate to click on that button
clickX := 545
clickY := 770

; How often (ms) to check
CheckInterval := 2000

; The color we consider "red" for the text. 
; AutoHotkey uses 0xBBGGRR in hex. "0xFF0000" means pure red in RGB.
healthColor := 0xFE1010

; The color we consider "solid grey" for the button.
solidGrey := 0x353535

; Variation for PixelSearch (0-255). Increase if colors are not exact.
redVariation := 20
greyVariation := 10

; ------------------------------------------------
; 2) Setup coordinate mode
; ------------------------------------------------
; We'll assume "Window" coordinates so that you can reposition the game window
; without having to recalculate the entire screen-based coordinates.
CoordMode, pixel, client

; ------------------------------------------------
; 3) Main Loop
; ------------------------------------------------
Loop
{
    ; Get the window's HWND
    WinGet, gameHwnd, ID, %GameTitle%
    if (!gameHwnd) {
        Tooltip, Game window not found for "%GameTitle%".
        Sleep, %CheckInterval%
        continue
    }

    ; ------------------------------------------------
    ; 3A) Check if health text region has "red" pixels
    ; ------------------------------------------------
    ; PixelSearch sets ErrorLevel=0 if found, 1 if not found, 2 if there's an error.
    PixelSearch, foundX, foundY
        , healthX1, healthY1, healthX2, healthY2
        , healthColor
        , redVariation, Fast RGB

    if (ErrorLevel = 0)
    {
        ; Found a red pixel => Health is likely low
        ; ------------------------------------------------
        ; 3B) Check if the button is "solid" (grey)
        ; ------------------------------------------------
        PixelSearch, foundX2, foundY2
            , buttonX1, buttonY1, buttonX2, buttonY2
            , solidGrey
            , greyVariation, Fast RGB

        if (ErrorLevel = 0)
        {
            ; Button appears to be "solid grey" => attempt to click
            ; We'll try ControlClick in the background (NA = No Activate).
            ; Note: Some games ignore this if they require actual focus.
            ControlClick, x%clickX% y%clickY%, ahk_id %gameHwnd%, , Left, 1, NA

            ; Optional: a small sleep or message
            ; MsgBox, "Clicked the solid grey button!"
        }
        else
        {
            ; The button is not "solid" or we didn't find the expected color
            ; You can log or debug here if needed
        }
    }
    else
    {
        ; Health is not red => do nothing
    }

    ; Wait before checking again
    Sleep, %CheckInterval%
}
