H:
cd h:\wav2lip-master
CALL C:\ProgramData\Miniconda3\Scripts\activate.bat C:\miniconda\envs\wave2lip
python inference.py --checkpoint ./checkpoints\wav2lip_gan.pth --face %1 --audio %2 --outfile %3
