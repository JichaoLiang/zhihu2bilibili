R:
cd r:\workspace\wave2lip
CALL C:\ProgramData\Miniconda3\Scripts\activate.bat C:\Users\Administrator\MiniConda3\envs\wave2lip
CALL conda activate wave2lip
C:\Users\Administrator\MiniConda3\envs\wave2lip\python.exe -V
C:\Users\Administrator\MiniConda3\envs\wave2lip\python.exe inference.py --checkpoint ./checkpoints\wav2lip.pth --face %1 --audio %2 --outfile %3
