import os.path

import torch
from sympy.physics.quantum.identitysearch import scipy
from torch import no_grad, LongTensor
from Utils.VITS import utils
from Utils.VITS import commons
from Utils.VITS.models import SynthesizerTrn
import soundfile as sf

from Utils.VITS.text import text_to_sequence, _clean_text


class Vits:
    net_g, hps, speaker_ids, speakers = None, None, None, None
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    voicemodel = {
        "shantianfang": {
            "modelpath": r"R:\workspace\model\vits\shantianfang\G_latest.pth",
            "configpath": r"R:\workspace\model\vits\shantianfang\modified_finetune_speaker.json"
        },
        "yeqiantong":{
            "modelpath": r"R:\workspace\model\vits\yeqiantong\G_latest.pth",
            "configpath": r"R:\workspace\model\vits\yeqiantong\finetune_speaker.json"
        }
    }

    language_marks = {
        "Japanese": "",
        "日本語": "[JA]",
        "简体中文": "[ZH]",
        "English": "[EN]",
        "Mix": "",
    }

    def get_text(self, text, hps, is_symbol):
        text_norm = text_to_sequence(text, hps.symbols, [] if is_symbol else hps.data.text_cleaners)
        if hps.data.add_blank:
            text_norm = commons.intersperse(text_norm, 0)
        text_norm = LongTensor(text_norm)
        return text_norm

    def vits_tts(self, text, speed, outputpath):
        speaker = self.speakers[0]
        text = self.language_marks["简体中文"] + text + self.language_marks["简体中文"]
        speaker_id = self.speaker_ids[speaker]
        stn_tst = self.get_text(text, self.hps, False)
        with no_grad():
            x_tst = stn_tst.unsqueeze(0).to(self.device)
            x_tst_lengths = LongTensor([stn_tst.size(0)]).to(self.device)
            sid = LongTensor([speaker_id]).to(self.device)
            audio = self.net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8,
                                     length_scale=1.0 / speed)[0][0, 0].data.cpu().float().numpy()
        del stn_tst, x_tst, x_tst_lengths, sid
        sf.write(outputpath, audio, self.hps.data.sampling_rate)
        return "Success", (self.hps.data.sampling_rate, audio)

    def loadModel(self, modelpath, configpath):
        self.hps = utils.get_hparams_from_file(configpath)
        self.net_g = SynthesizerTrn(
            len(self.hps.symbols),
            self.hps.data.filter_length // 2 + 1,
            self.hps.train.segment_size // self.hps.data.hop_length,
            n_speakers=self.hps.data.n_speakers,
            **self.hps.model).to(self.device)
        _ = self.net_g.eval()

        _ = utils.load_checkpoint(modelpath, self.net_g, None)
        self.speaker_ids = self.hps.speakers
        self.speakers = list(self.hps.speakers.keys())


if __name__ == '__main__':
    modelpath = r"Q:\baiduNetdisk\tts整合包\.VITS\VITS-barbara\VITS-barbara\OUTPUT_MODEL\G_latest.pth"
    configpath = r"Q:\baiduNetdisk\tts整合包\.VITS\VITS-barbara\VITS-barbara\configs\modified_finetune_speaker.json"
    outputpath = r"Q:\test"
    vits = Vits()
    vits.loadModel(modelpath=modelpath, configpath=configpath)
    while True:
        inputStr = input("text: ")
        if inputStr.lower() == 'exit':
            break
        name = inputStr
        if len(name) > 5:
            name = name[0:5]
        outputpath = os.path.join(outputpath, name + ".wav")
        vits.vits_tts(inputStr, 0.7, outputpath)
