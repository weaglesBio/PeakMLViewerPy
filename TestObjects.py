from Data.PeakML.PeakML import PeakML
from Data.PeakML.Header import Header
from Data.PeakML.Peak import Peak
from Data.PeakML.SetInfo import SetInfo
from Data.PeakML.FileInfo import FileInfo
from Data.PeakML.ScanInfo import ScanInfo
from Data.PeakML.MeasurementInfo import MeasurementInfo
from Data.PeakML.Annotation import Annotation
from Data.PeakML.PeakData import PeakData

import base64

def get_test_peakml_obj() -> PeakML:


    header = Header(959, 'November 16, 2018', None, None)

    sets = []
    measurements = []

#    (self, id: int, type: str, measurement_ids_byte_array: bytearray)

    set_me_bl = ['0.0' '2.3509887e-38']
    set_me_ibe = ['9.403955e-38' '3.761582e-37' '1.5046328e-36']
    set_me_ibu = ['6.018531e-36' '2.4074124e-35' '9.62965e-35']
    set_me_igr = ['3.85186e-34' '1.540744e-33' '6.162976e-33']
    set_me_iol = ['2.4651903e-32' '9.8607613e-32' '3.9443045e-31']
    set_me_ipu = ['1.009742e-28' '4.038968e-28' '1.6155871e-27']
    set_me_ith = ['6.4623485e-27' '2.5849394e-26' '1.0339758e-25']
    set_me_lbe = ['4.135903e-25' '1.6543612e-24' '6.617445e-24']
    set_me_lbu = ['2.646978e-23' '1.0587912e-22' '4.2351647e-22']
    set_me_lco = ['1.6940659e-21' '6.7762636e-21' '2.7105054e-20']
    set_me_les = ['1.0842022e-19' '4.3368087e-19' '1.7347235e-18']
    set_me_lpe = ['6.938894e-18' '2.7755576e-17' '1.110223e-16']
    set_me_lsa = ['2.842171e-14' '1.1368684e-13' '4.5474735e-13']
    set_me_pbr = ['1.8189894e-12' '7.275958e-12' '2.910383e-11']
    set_me_pco = ['1.1641532e-10' '4.656613e-10' '1.8626451e-09']
    set_me_pdr = ['7.450581e-09' '2.9802322e-08' '1.1920929e-07']
    set_me_pgu = ['4.7683716e-07' '1.9073486e-06' '7.6293945e-06']
    set_me_plo = ['3.0517578e-05' '0.00012207031' '0.00048828125']
    set_me_pro = ['0.001953125' '0.0078125' '0.03125']
    set_me_pwh = ['0.125' '0.5' '2.0']
    set_me_qc = ['8.0' '32.0' '128.0' '512.0' '2048.0' '8192.0' '32768.0' '131072.0' '524288.0' '2097152.0' '8388608.0' '33554432.0' '134217730.0' '536870900.0' '2147483600.0' '8589935000.0' '34359740000.0' '137438950000.0' '549755800000.0' '2199023300000.0' '8796093000000.0']

    sets.append(SetInfo("Blank", 0, set_me_bl))
    sets.append(SetInfo("IPA_Beard","0", set_me_ibe))
    sets.append(SetInfo("IPA_Bust","0", set_me_ibu))
    sets.append(SetInfo("IPA_Green","0", set_me_igr))
    sets.append(SetInfo("IPA_Old","0", set_me_iol))
    sets.append(SetInfo("IPA_Punk","0", set_me_ipu))
    sets.append(SetInfo("IPA_Thorn","0", set_me_ith))
    sets.append(SetInfo("Lag_Beck","0", set_me_lbe))
    sets.append(SetInfo("Lag_Bud","0", set_me_lbu))
    sets.append(SetInfo("Lag_Cob","0", set_me_lco))
    sets.append(SetInfo("Lag_Est","0", set_me_les))
    sets.append(SetInfo("Lag_Per","0", set_me_lpe))
    sets.append(SetInfo("Lag_San","0", set_me_lsa))
    sets.append(SetInfo("Port_Brew","0", set_me_pbr))
    sets.append(SetInfo("Port_Coffee","0", set_me_pco))
    sets.append(SetInfo("Port_Drag","0", set_me_pdr))
    sets.append(SetInfo("Port_Guin","0", set_me_pgu))
    sets.append(SetInfo("Port_Lond","0", set_me_plo))
    sets.append(SetInfo("Port_Rob","0", set_me_pro))
    sets.append(SetInfo("Port_White","0", set_me_pwh))
    sets.append(SetInfo("QC","0", set_me_qc))

    #id: int, label: str, sample_id: str

    measurement = MeasurementInfo(0, "Blank_01b_POS", "Blank_01b_POS")
    scan = ScanInfo("POSITIVE","0.301082772")
    scan.add_annotation(Annotation("", None, "RT_raw", "0.301082772", "STRING"))
    #self, polarity: int, retention_time: str
    measurement.add_scan(scan)
    #self, label: str, name: str, location: str
    measurement.add_file(FileInfo("Blank_01b_POS.mzML","Blank_01b_POS.mzML","/home/mqbpqfd2/.dropbox-alt/Dropbox (The University of Manchester)/IPA_code&amp;manuscript/Beer_dataset/./data/Blank"))
    measurements.append(measurement)

    measurements.append(MeasurementInfo(1, "Blank_01c_POS", "Blank_01c_POS"))
    measurements.append(MeasurementInfo(2, "IPA_Beard_POS_1", "IPA_Beard_POS_1"))
    measurements.append(MeasurementInfo(3, "IPA_Beard_POS_2", "IPA_Beard_POS_2"))
    measurements.append(MeasurementInfo(4, "IPA_Beard_POS_3", "IPA_Beard_POS_3"))
    measurements.append(MeasurementInfo(5, "IPA_Bust_POS_1", "IPA_Bust_POS_1"))
    measurements.append(MeasurementInfo(6, "IPA_Bust_POS_2", "IPA_Bust_POS_2"))
    measurements.append(MeasurementInfo(7, "IPA_Bust_POS_3", "IPA_Bust_POS_3"))
    measurements.append(MeasurementInfo(8, "IPA_Green_POS_1", "IPA_Green_POS_1"))
    measurements.append(MeasurementInfo(9, "IPA_Green_POS_2", "IPA_Green_POS_2"))
    measurements.append(MeasurementInfo(10, "IPA_Green_POS_3", "IPA_Green_POS_3"))
    measurements.append(MeasurementInfo(11, "IPA_Hob_POS_1", "IPA_Hob_POS_1"))
    measurements.append(MeasurementInfo(12, "IPA_Hob_POS_2", "IPA_Hob_POS_2"))
    measurements.append(MeasurementInfo(13, "IPA_Hob_POS_3", "IPA_Hob_POS_3"))
    measurements.append(MeasurementInfo(14, "IPA_Old_POS_1", "IPA_Old_POS_1"))
    measurements.append(MeasurementInfo(15, "IPA_Old_POS_2", "IPA_Old_POS_2"))
    measurements.append(MeasurementInfo(16, "IPA_Old_POS_3", "IPA_Old_POS_3"))
    measurements.append(MeasurementInfo(17, "IPA_Punk_POS_1", "IPA_Punk_POS_1"))
    measurements.append(MeasurementInfo(18, "IPA_Punk_POS_2", "IPA_Punk_POS_2"))
    measurements.append(MeasurementInfo(19, "IPA_Punk_POS_3", "IPA_Punk_POS_3"))
    measurements.append(MeasurementInfo(20, "IPA_Thorn_POS_1", "IPA_Thorn_POS_1"))
    measurements.append(MeasurementInfo(21, "IPA_Thorn_POS_2", "IPA_Thorn_POS_2"))
    measurements.append(MeasurementInfo(22, "IPA_Thorn_POS_3", "IPA_Thorn_POS_3"))
    measurements.append(MeasurementInfo(23, "Lag_Beck_POS_1", "Lag_Beck_POS_1"))
    measurements.append(MeasurementInfo(24, "Lag_Beck_POS_2", "Lag_Beck_POS_2"))
    measurements.append(MeasurementInfo(25, "Lag_Beck_POS_3", "Lag_Beck_POS_3"))
    measurements.append(MeasurementInfo(26, "Lag_Bud_POS_1", "Lag_Bud_POS_1"))
    measurements.append(MeasurementInfo(27, "Lag_Bud_POS_2", "Lag_Bud_POS_2"))
    measurements.append(MeasurementInfo(28, "Lag_Bud_POS_3", "Lag_Bud_POS_3"))
    measurements.append(MeasurementInfo(29, "Lag_Cob_POS_1", "Lag_Cob_POS_1"))
    measurements.append(MeasurementInfo(30, "Lag_Cob_POS_2", "Lag_Cob_POS_2"))
    measurements.append(MeasurementInfo(31, "Lag_Cob_POS_3", "Lag_Cob_POS_3"))
    measurements.append(MeasurementInfo(32, "Lag_Est_POS_1", "Lag_Est_POS_1"))
    measurements.append(MeasurementInfo(33, "Lag_Est_POS_2", "Lag_Est_POS_2"))
    measurements.append(MeasurementInfo(34, "Lag_Est_POS_3", "Lag_Est_POS_3"))
    measurements.append(MeasurementInfo(35, "Lag_Hop_POS_1", "Lag_Hop_POS_1"))
    measurements.append(MeasurementInfo(36, "Lag_Hop_POS_2", "Lag_Hop_POS_2"))
    measurements.append(MeasurementInfo(37, "Lag_Hop_POS_3", "Lag_Hop_POS_3"))
    measurements.append(MeasurementInfo(38, "Lag_Per_POS_1", "Lag_Per_POS_1"))
    measurements.append(MeasurementInfo(39, "Lag_Per_POS_2", "Lag_Per_POS_2"))
    measurements.append(MeasurementInfo(40, "Lag_Per_POS_3", "Lag_Per_POS_3"))
    measurements.append(MeasurementInfo(41, "Lag_San_POS_1", "Lag_San_POS_1"))
    measurements.append(MeasurementInfo(42, "Lag_San_POS_2", "Lag_San_POS_2"))
    measurements.append(MeasurementInfo(43, "Lag_San_POS_3", "Lag_San_POS_3"))
    measurements.append(MeasurementInfo(44, "Port_Brew_POS_1", "Port_Brew_POS_1"))
    measurements.append(MeasurementInfo(45, "Port_Brew_POS_2", "Port_Brew_POS_2"))
    measurements.append(MeasurementInfo(46, "Port_Brew_POS_3", "Port_Brew_POS_3"))
    measurements.append(MeasurementInfo(47, "Port_Coffee_POS_1", "Port_Coffee_POS_1"))
    measurements.append(MeasurementInfo(48, "Port_Coffee_POS_2", "Port_Coffee_POS_2"))
    measurements.append(MeasurementInfo(49, "Port_Coffee_POS_3", "Port_Coffee_POS_3"))
    measurements.append(MeasurementInfo(50, "Port_Drag_POS_1", "Port_Drag_POS_1"))
    measurements.append(MeasurementInfo(51, "Port_Drag_POS_2", "Port_Drag_POS_2"))
    measurements.append(MeasurementInfo(52, "Port_Drag_POS_3", "Port_Drag_POS_3"))
    measurements.append(MeasurementInfo(53, "Port_Guin_POS_1", "Port_Guin_POS_1"))
    measurements.append(MeasurementInfo(54, "Port_Guin_POS_2", "Port_Guin_POS_2"))
    measurements.append(MeasurementInfo(55, "Port_Guin_POS_3", "Port_Guin_POS_3"))
    measurements.append(MeasurementInfo(56, "Port_Lond_POS_1", "Port_Lond_POS_1"))
    measurements.append(MeasurementInfo(57, "Port_Lond_POS_2", "Port_Lond_POS_2"))
    measurements.append(MeasurementInfo(58, "Port_Lond_POS_3", "Port_Lond_POS_3"))
    measurements.append(MeasurementInfo(59, "Port_Rob_POS_1", "Port_Rob_POS_1"))
    measurements.append(MeasurementInfo(60, "Port_Rob_POS_2", "Port_Rob_POS_2"))
    measurements.append(MeasurementInfo(61, "Port_Rob_POS_3", "Port_Rob_POS_3"))
    measurements.append(MeasurementInfo(62, "Port_White_POS_1", "Port_White_POS_1"))
    measurements.append(MeasurementInfo(63, "Port_White_POS_2", "Port_White_POS_2"))
    measurements.append(MeasurementInfo(64, "Port_White_POS_3", "Port_White_POS_3"))
    measurements.append(MeasurementInfo(65, "QC01_POS", "QC01_POS"))
    measurements.append(MeasurementInfo(66, "QC02_POS", "QC02_POS"))
    measurements.append(MeasurementInfo(67, "QC03_POS", "QC03_POS"))
    measurements.append(MeasurementInfo(68, "QC04_POS", "QC04_POS"))
    measurements.append(MeasurementInfo(69, "QC05_POS", "QC05_POS"))
    measurements.append(MeasurementInfo(70, "QC06_POS", "QC06_POS"))
    measurements.append(MeasurementInfo(71, "QC07_POS", "QC07_POS"))
    measurements.append(MeasurementInfo(72, "QC08_POS", "QC08_POS"))
    measurements.append(MeasurementInfo(73, "QC09_POS", "QC09_POS"))
    measurements.append(MeasurementInfo(74, "QC10_POS", "QC10_POS"))
    measurements.append(MeasurementInfo(75, "QC11_POS", "QC11_POS"))
    measurements.append(MeasurementInfo(76, "QC12_POS", "QC12_POS"))
    measurements.append(MeasurementInfo(77, "QC13_POS", "QC13_POS"))
    measurements.append(MeasurementInfo(78, "QC14_POS", "QC14_POS"))
    measurements.append(MeasurementInfo(79, "QC15_POS", "QC15_POS"))
    measurements.append(MeasurementInfo(80, "QC16_POS", "QC16_POS"))
    measurements.append(MeasurementInfo(81, "QC17_POS", "QC17_POS"))
    measurements.append(MeasurementInfo(82, "QC18_POS", "QC18_POS"))
    measurements.append(MeasurementInfo(83, "QC19_POS", "QC19_POS"))
    measurements.append(MeasurementInfo(84, "QC20_POS", "QC20_POS"))
    measurements.append(MeasurementInfo(85, "QC21_POS", "QC21_POS"))

    #self, type: str, scan: str, retention_time: str, mass: float, intensity: float, measurement_id: str, pattern_id: str, sha1sum: str, signal: str, peak_data: PeakData
    peakset_1 = Peak("peakset","142", "45.770422824593474", "116.0705470217265","2.170016768E9","0","nu3EG1Q94I1uB0xidE1CSmv3nKU", None, None)

    # self, unit: str = "", ontology_ref: str = "", label: str = "", value: str = "", value_type: str = "STRING"
    peakset_1.add_annotation(Annotation("", None, "charge", "1", "STRING"))
    peakset_1.add_annotation(Annotation("", None, "codadw", "0.9855825132969098", "STRING"))
    peakset_1.add_annotation(Annotation("", None, "id", "1", "STRING"))
    peakset_1.add_annotation(Annotation("", None, "relation.ship", "bp", "STRING"))
    peakset_1.add_annotation(Annotation("", None, "relation.id", "0", "INTEGER"))

    peak_data_1_1 = PeakData("centroid", 29)
    peak_data_1_1.scan_ids = [1.661535e+35, 6.64614e+35, 2.658456e+36, 1.0633824e+37, 4.2535296e+37, 1.7014118e+38, -0.0, -2.3509887e-38, -9.403955e-38, -3.761582e-37, -1.5046328e-36, -6.018531e-36, -2.4074124e-35, -9.62965e-35, -3.85186e-34, -1.540744e-33, -6.162976e-33, -2.4651903e-32, -9.8607613e-32, -3.9443045e-31, -1.5777218e-30, -6.3108872e-30, -2.524355e-29, -1.009742e-28, -4.038968e-28, -1.6155871e-27, -6.4623485e-27, -2.5849394e-26, -1.0339758e-25]
    peak_data_1_1.retention_times = [41.690308, 42.02792, 42.363163, 42.696915, 43.030926, 43.362156, 43.695404, 44.028294, 44.361393, 44.693768, 45.028152, 45.364513, 45.701015, 46.037403, 46.371635, 46.705757, 47.038635, 47.375378, 47.711, 48.04551, 48.381245, 48.717995, 49.055, 49.39199, 49.727486, 50.06375, 50.399605, 50.73448, 51.070488]
    peak_data_1_1.masses = [116.070465, 116.07055, 116.07059, 116.070694, 116.07061, 116.07064, 116.07064, 116.07061, 116.0706, 116.07058, 116.07057, 116.07059, 116.070564, 116.07055, 116.07059, 116.07056, 116.07056, 116.07057, 116.07057, 116.07059, 116.07058, 116.07057, 116.070595, 116.070625, 116.07065, 116.070625, 116.07058, 116.07058, 116.07056]
    peak_data_1_1.intensities = [25921.293, 40214.902, 35398.594, 42223.715, 41771.75, 40701.773, 75635.02, 214720.58, 623022.6, 1158793.2, 1613674.8, 1822454.2, 1702354.6, 1509551.2, 1316949.4, 1049980.0, 857840.94, 620042.06, 480598.25, 365535.12, 238095.89, 194545.72, 140767.61, 106037.89, 93690.18, 60245.723, 71683.7, 48273.336, 55255.754]
    peak_data_1_1.relative_intensities = [25921.293, 40214.902, 35398.594, 42223.715, 41771.75, 40701.773, 75635.02, 214720.58, 623022.6, 1158793.2, 1613674.8, 1822454.2, 1702354.6, 1509551.2, 1316949.4, 1049980.0, 857840.94, 620042.06, 480598.25, 365535.12, 238095.89, 194545.72, 140767.61, 106037.89, 93690.18, 60245.723, 71683.7, 48273.336, 55255.754]
    peak_data_1_1.pattern_ids = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    peak_data_1_1.measurement_ids = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    peakset_1.peaks.append(Peak("masschromatogram", "133", "45.3645133972168", "116.07057825577071", "1822454.25", "0", None, peak_data_1_1))

    peak_data_1_2 = PeakData("centroid", 29)
    peak_data_1_2.scan_ids = [4.1538375e+34, 1.661535e+35, 6.64614e+35, 2.658456e+36, 1.0633824e+37, 4.2535296e+37, 1.7014118e+38, -0.0, -2.3509887e-38, -9.403955e-38, -3.761582e-37, -1.5046328e-36, -6.018531e-36, -2.4074124e-35, -9.62965e-35, -3.85186e-34, -1.540744e-33, -6.162976e-33, -2.4651903e-32, -9.8607613e-32, -3.9443045e-31, -1.5777218e-30, -6.3108872e-30, -2.524355e-29, -1.009742e-28, -4.038968e-28, -1.6155871e-27, -6.4623485e-27, -2.5849394e-26]
    peak_data_1_2.retention_times = [41.585052, 41.926537, 42.26703, 42.60954, 42.951153, 43.290524, 43.62979, 43.9689, 44.310646, 44.650906, 44.99091, 45.33076, 45.669506, 46.008015, 46.34613, 46.687004, 47.03014, 47.373386, 47.714867, 48.059254, 48.400124, 48.741116, 49.085365, 49.430122, 49.77286, 50.11398, 50.45699, 50.82586, 51.1671]
    peak_data_1_2.masses = [116.0706, 116.07062, 116.07058, 116.07063, 116.07062, 116.07064, 116.07063, 116.07063, 116.07062, 116.07063, 116.0706, 116.070595, 116.07058, 116.07059, 116.07059, 116.07057, 116.07055, 116.07058, 116.0706, 116.07058, 116.070625, 116.070595, 116.07065, 116.0706, 116.0706, 116.070625, 116.07071, 116.07054, 116.070625]
    peak_data_1_2.intensities = [37045.773, 29975.553, 30083.76, 34624.16, 34730.49, 40838.992, 87394.41, 256950.08, 727941.7, 1292766.8, 1809856.2, 1874645.8, 1822056.9, 1533788.8, 1278701.0, 1062779.6, 795797.25, 597781.56, 462186.53, 309275.62, 237721.55, 155500.67, 114054.266, 94666.73, 61067.207, 64240.066, 59993.6, 37245.35, 45588.55]
    peak_data_1_2.relative_intensities = [37045.773, 29975.553, 30083.76, 34624.16, 34730.49, 40838.992, 87394.41, 256950.08, 727941.7, 1292766.8, 1809856.2, 1874645.8, 1822056.9, 1533788.8, 1278701.0, 1062779.6, 795797.25, 597781.56, 462186.53, 309275.62, 237721.55, 155500.67, 114054.266, 94666.73, 61067.207, 64240.066, 59993.6, 37245.35, 45588.55]
    peak_data_1_2.pattern_ids = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    peak_data_1_2.measurement_ids = [2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38]

    peakset_1.peaks.append(Peak("masschromatogram", "132", "45.33076095581055", "116.0705979739929", "1874645.75", "1", None, peak_data_1_2))

    peak_data_1_3 = PeakData("centroid", 33)
    peak_data_1_3.scan_ids = [-2.3509887e-38, -9.403955e-38, -3.761582e-37, -1.5046328e-36, -6.018531e-36, -2.4074124e-35, -9.62965e-35, -3.85186e-34, -1.540744e-33, -6.162976e-33, -2.4651903e-32, -9.8607613e-32, -3.9443045e-31, -1.5777218e-30, -6.3108872e-30, -2.524355e-29, -1.009742e-28, -4.038968e-28, -1.6155871e-27, -6.4623485e-27, -2.5849394e-26, -1.0339758e-25, -4.135903e-25, -1.6543612e-24, -6.617445e-24, -2.646978e-23, -1.0587912e-22, -4.2351647e-22, -1.6940659e-21, -6.7762636e-21, -2.7105054e-20, -1.0842022e-19, -4.3368087e-19]
    peak_data_1_3.retention_times = [41.56396, 41.867462, 42.170956, 42.4741, 42.77683, 43.07947, 43.38145, 43.683586, 43.98582, 44.288204, 44.590565, 44.89295, 45.195312, 45.498188, 45.80093, 46.103573, 46.406303, 46.70907, 47.011925, 47.315437, 47.618797, 47.92231, 48.226795, 48.531166, 48.835915, 49.140163, 49.444412, 49.74853, 50.053158, 50.35778, 50.662773, 50.968395, 51.274776]
    peak_data_1_3.masses = [116.07039, 116.070404, 116.070435, 116.070564, 116.0707, 116.0707, 116.07066, 116.07064, 116.07063, 116.07062, 116.0706, 116.07057, 116.070526, 116.07048, 116.070496, 116.07049, 116.07049, 116.07049, 116.070465, 116.07044, 116.07047, 116.07047, 116.07049, 116.07046, 116.07045, 116.07044, 116.07045, 116.070435, 116.070465, 116.07044, 116.07044, 116.07046, 116.07045]
    peak_data_1_3.intensities = [3228541.0, 2159621.8, 1665104.0, 1207089.8, 868555.44, 1913858.1, 8489078.0, 32558016.0, 129702650.0, 282196860.0, 478786370.0, 615665100.0, 807587500.0, 864462800.0, 795052740.0, 825430900.0, 820100200.0, 785153600.0, 668149900.0, 580187260.0, 477236900.0, 427192100.0, 328034700.0, 272324300.0, 208986830.0, 144598690.0, 109757270.0, 71938504.0, 53741310.0, 48628040.0, 46153508.0, 43630976.0, 43329844.0]
    peak_data_1_3.relative_intensities = [3228541.0, 2159621.8, 1665104.0, 1207089.8, 868555.44, 1913858.1, 8489078.0, 32558016.0, 129702650.0, 282196860.0, 478786370.0, 615665100.0, 807587500.0, 864462800.0, 795052740.0, 825430900.0, 820100200.0, 785153600.0, 668149900.0, 580187260.0, 477236900.0, 427192100.0, 328034700.0, 272324300.0, 208986830.0, 144598690.0, 109757270.0, 71938504.0, 53741310.0, 48628040.0, 46153508.0, 43630976.0, 43329844.0]
    peak_data_1_3.pattern_ids = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    peak_data_1_3.measurement_ids = [9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38]
    peakset_1.peaks.append(Peak("masschromatogram", "142", "45.49818801879883", "116.07050034996007", "8.64462784E8", "2", None, peak_data_1_3))

    peak_data_1_4 = PeakData("centroid", 32)
    peak_data_1_4.scan_ids = [-3.761582e-37, -1.5046328e-36, -6.018531e-36, -2.4074124e-35, -9.62965e-35, -3.85186e-34, -1.540744e-33, -6.162976e-33, -2.4651903e-32, -9.8607613e-32, -3.9443045e-31, -1.5777218e-30, -6.3108872e-30, -2.524355e-29, -1.009742e-28, -4.038968e-28, -1.6155871e-27, -6.4623485e-27, -2.5849394e-26, -1.0339758e-25, -4.135903e-25, -1.6543612e-24, -6.617445e-24, -2.646978e-23, -1.0587912e-22, -4.2351647e-22, -1.6940659e-21, -6.7762636e-21, -2.7105054e-20, -1.0842022e-19, -4.3368087e-19, -1.7347235e-18]
    peak_data_1_4.retention_times = [41.769325, 42.072334, 42.374943, 42.677322, 42.97956, 43.281708, 43.58394, 43.8862, 44.188683, 44.490944, 44.793175, 45.095806, 45.3983, 45.701187, 46.0038, 46.30667, 46.609543, 46.912666, 47.215916, 47.519535, 47.823284, 48.12703, 48.4309, 48.734898, 49.039146, 49.343025, 49.64677, 49.950893, 50.255154, 50.560013, 50.86477, 51.170506]
    peak_data_1_4.masses = [116.07047, 116.070526, 116.07067, 116.07079, 116.070816, 116.07081, 116.07078, 116.07074, 116.070694, 116.070656, 116.07062, 116.070625, 116.070595, 116.07058, 116.07056, 116.07053, 116.07055, 116.07055, 116.070526, 116.07052, 116.07054, 116.070526, 116.07054, 116.07049, 116.07049, 116.070465, 116.070496, 116.07043, 116.07049, 116.07053, 116.07081, 116.0708]
    peak_data_1_4.intensities = [2390385.5, 1689079.9, 1763055.8, 1179225.1, 2637987.0, 11631014.0, 46929644.0, 167484620.0, 334743260.0, 560920800.0, 765842560.0, 944465700.0, 942957800.0, 940621760.0, 931873340.0, 928841500.0, 860331300.0, 707271400.0, 628473000.0, 540854500.0, 438690020.0, 373872700.0, 279361380.0, 244548110.0, 164778560.0, 118933300.0, 83614220.0, 57124304.0, 53942056.0, 49213850.0, 52884904.0, 47803564.0]
    peak_data_1_4.relative_intensities = [2390385.5, 1689079.9, 1763055.8, 1179225.1, 2637987.0, 11631014.0, 46929644.0, 167484620.0, 334743260.0, 560920800.0, 765842560.0, 944465700.0, 942957800.0, 940621760.0, 931873340.0, 928841500.0, 860331300.0, 707271400.0, 628473000.0, 540854500.0, 438690020.0, 373872700.0, 279361380.0, 244548110.0, 164778560.0, 118933300.0, 83614220.0, 57124304.0, 53942056.0, 49213850.0, 52884904.0, 47803564.0]
    peak_data_1_4.pattern_ids = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    peak_data_1_4.measurement_ids = [3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37]
    peakset_1.peaks.append(Peak("masschromatogram", "142", "45.09580612182617", "116.07057947895528", "9.44465728E8", "3", None, peak_data_1_4))

    peak_data_1_5 = PeakData("centroid", 33)
    peak_data_1_5.scan_ids = [-9.403955e-38, -3.761582e-37, -1.5046328e-36, -6.018531e-36, -2.4074124e-35, -9.62965e-35, -3.85186e-34, -1.540744e-33, -6.162976e-33, -2.4651903e-32, -9.8607613e-32, -3.9443045e-31, -1.5777218e-30, -6.3108872e-30, -2.524355e-29, -1.009742e-28, -4.038968e-28, -1.6155871e-27, -6.4623485e-27, -2.5849394e-26, -1.0339758e-25, -4.135903e-25, -1.6543612e-24, -6.617445e-24, -2.646978e-23, -1.0587912e-22, -4.2351647e-22, -1.6940659e-21, -6.7762636e-21, -2.7105054e-20, -1.0842022e-19, -4.3368087e-19, -1.7347235e-18]
    peak_data_1_5.retention_times = [41.57062, 41.87375, 42.17687, 42.479744, 42.782238, 43.084488, 43.386734, 43.68873, 43.991104, 44.293358, 44.59585, 44.898228, 45.200844, 45.50322, 45.805965, 46.108345, 46.410847, 46.713844, 47.016594, 47.319714, 47.623215, 47.92671, 48.23046, 48.534325, 48.838455, 49.142445, 49.446323, 49.75007, 50.0542, 50.358315, 50.66294, 50.96781, 51.273804]
    peak_data_1_5.masses = [116.07049, 116.07048, 116.07054, 116.07061, 116.07071, 116.07077, 116.07076, 116.07075, 116.07076, 116.07078, 116.07071, 116.07066, 116.07064, 116.07061, 116.07059, 116.070595, 116.07058, 116.07053, 116.070564, 116.07052, 116.0705, 116.07052, 116.07052, 116.070526, 116.070564, 116.07049, 116.0705, 116.07049, 116.07051, 116.07052, 116.07051, 116.07049, 116.070496]
    peak_data_1_5.intensities = [3431316.5, 2301369.0, 1811683.6, 1219889.2, 1039318.6, 1950798.5, 6940779.5, 28742028.0, 109657730.0, 264511020.0, 473706020.0, 710983550.0, 841786400.0, 949660900.0, 1000107800.0, 859286400.0, 884971970.0, 815538000.0, 724164400.0, 643758140.0, 553793400.0, 473425200.0, 388935400.0, 298245630.0, 233485300.0, 177045380.0, 123467384.0, 92669550.0, 59416040.0, 55378892.0, 49398436.0, 46352148.0, 42016148.0]
    peak_data_1_5.relative_intensities = [3431316.5, 2301369.0, 1811683.6, 1219889.2, 1039318.6, 1950798.5, 6940779.5, 28742028.0, 109657730.0, 264511020.0, 473706020.0, 710983550.0, 841786400.0, 949660900.0, 1000107800.0, 859286400.0, 884971970.0, 815538000.0, 724164400.0, 643758140.0, 553793400.0, 473425200.0, 388935400.0, 298245630.0, 233485300.0, 177045380.0, 123467384.0, 92669550.0, 59416040.0, 55378892.0, 49398436.0, 46352148.0, 42016148.0]
    peak_data_1_5.pattern_ids = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    peak_data_1_5.measurement_ids = [1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36]
    peakset_1.peaks.append(Peak("masschromatogram", "144", "45.805965423583984", "116.07058390185306", "1.000107776E9", "4", None, peak_data_1_5))

    #self, type: str, scan: str, retention_time: str, mass: float, intensity: float, measurement_id: str, pattern_id: str, sha1sum: str, signal: str, peak_data: PeakData
    peakset_2 = Peak("peakset","142", "45.78758563551792", "117.0736908526656","1.2565204E8","80","/x6XWUHgs9ZpBrMotF1emKG0hL8=", None, None)

    # self, unit: str = "", ontology_ref: str = "", label: str = "", value: str = "", value_type: str = "STRING"
    peakset_2.add_annotation(Annotation("", None, "codadw", "0.9848288770510563", "STRING"))
    peakset_2.add_annotation(Annotation("", None, "id", "88", "STRING"))
    peakset_2.add_annotation(Annotation("", None, "relation.ship", "bp|C13 isotope #1", "STRING"))
    peakset_2.add_annotation(Annotation("", None, "relation.id", "0", "INTEGER"))

    peak_data_2_1 = PeakData("centroid", 21)
    peak_data_2_1.scan_ids = [1.0633824e+37, 4.2535296e+37, -2.3509887e-38, -9.403955e-38, -3.761582e-37, -1.5046328e-36, -6.018531e-36, -2.4074124e-35, -9.62965e-35, -3.85186e-34, -1.540744e-33, -6.162976e-33, -2.4651903e-32, -9.8607613e-32, -3.9443045e-31, -1.5777218e-30, -6.3108872e-30, -2.524355e-29, -1.009742e-28, -4.038968e-28, -1.6155871e-27]
    peak_data_2_1.retention_times = [42.696915, 43.030926, 44.028294, 44.361393, 44.693768, 45.028152, 45.364513, 45.701015, 46.037403, 46.371635, 46.705757, 47.038635, 47.375378, 47.711, 48.04551, 48.381245, 48.717995, 49.055, 49.39199, 49.727486, 50.06375]
    peak_data_2_1.masses = [117.0739, 117.07397, 117.07391, 117.073906, 117.07388, 117.07388, 117.0739, 117.07385, 117.07385, 117.07394, 117.0739, 117.073875, 117.07392, 117.07387, 117.07395, 117.07393, 117.07396, 117.074, 117.07397, 117.074165, 117.07388]
    peak_data_2_1.intensities = [4214.1357, 3709.2144, 15577.108, 42766.51, 66390.53, 96011.1, 106359.96, 87735.32, 90817.016, 72756.27, 59130.836, 47146.535, 30820.492, 22365.73, 21103.033, 15057.236, 14638.187, 4012.398, 3104.6052, 3471.1099, 2673.6643]
    peak_data_2_1.relative_intensities = [4214.1357, 3709.2144, 15577.108, 42766.51, 66390.53, 96011.1, 106359.96, 87735.32, 90817.016, 72756.27, 59130.836, 47146.535, 30820.492, 22365.73, 21103.033, 15057.236, 14638.187, 4012.398, 3104.6052, 3471.1099, 2673.6643]
    peak_data_2_1.pattern_ids = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    peak_data_2_1.measurement_ids = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    peakset_2.peaks.append(Peak("masschromatogram", "133", "45.3645133972168", "117.07389897416458", "106359.9609375", "0", None, peak_data_2_1))

    peak_data_2_2 = PeakData("centroid", 16)
    peak_data_2_2.scan_ids = [-0.0, -2.3509887e-38, -9.403955e-38, -3.761582e-37, -1.5046328e-36, -6.018531e-36, -2.4074124e-35, -9.62965e-35, -3.85186e-34, -1.540744e-33, -6.162976e-33, -2.4651903e-32, -9.8607613e-32, -3.9443045e-31, -1.5777218e-30, -6.3108872e-30]
    peak_data_2_2.retention_times = [43.9689, 44.310646, 44.650906, 44.99091, 45.33076, 45.669506, 46.008015, 46.34613, 46.687004, 47.03014, 47.373386, 47.714867, 48.059254, 48.400124, 48.741116, 49.085365]
    peak_data_2_2.masses = [117.07408, 117.07393, 117.07401, 117.073944, 117.07392, 117.07389, 117.07389, 117.07392, 117.07389, 117.07392, 117.07392, 117.07398, 117.0739, 117.073875, 117.07388, 117.073944]
    peak_data_2_2.intensities = [12170.031, 37173.797, 70659.875, 98298.914, 95047.81, 97490.93, 82766.195, 57327.5, 49063.508, 43944.914, 36226.848, 17386.262, 20707.33, 5957.942, 10325.604, 3352.1453]
    peak_data_2_2.relative_intensities = [12170.031, 37173.797, 70659.875, 98298.914, 95047.81, 97490.93, 82766.195, 57327.5, 49063.508, 43944.914, 36226.848, 17386.262, 20707.33, 5957.942, 10325.604, 3352.1453]
    peak_data_2_2.pattern_ids = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    peak_data_2_2.measurement_ids = [2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38]
    peakset_2.peaks.append(Peak("masschromatogram", "133", "44.990909576416016", "117.07392725188726", "98298.9140625", "1", None, peak_data_2_2))

    peak_data_2_3 = PeakData("centroid", 27)
    peak_data_2_3.scan_ids = [-9.403955e-38, -3.85186e-34, -1.540744e-33, -6.162976e-33, -2.4651903e-32, -9.8607613e-32, -3.9443045e-31, -1.5777218e-30, -6.3108872e-30, -2.524355e-29, -1.009742e-28, -4.038968e-28, -1.6155871e-27, -6.4623485e-27, -2.5849394e-26, -1.0339758e-25, -4.135903e-25, -1.6543612e-24, -6.617445e-24, -2.646978e-23, -1.0587912e-22, -4.2351647e-22, -1.6940659e-21, -6.7762636e-21, -2.7105054e-20, -1.0842022e-19, -4.3368087e-19]
    peak_data_2_3.retention_times = [41.867462, 43.683586, 43.98582, 44.288204, 44.590565, 44.89295, 45.195312, 45.498188, 45.80093, 46.103573, 46.406303, 46.70907, 47.011925, 47.315437, 47.618797, 47.92231, 48.226795, 48.531166, 48.835915, 49.140163, 49.444412, 49.74853, 50.053158, 50.35778, 50.662773, 50.968395, 51.274776]
    peak_data_2_3.masses = [117.07374, 117.07395, 117.07394, 117.07391, 117.07384, 117.073784, 117.0737, 117.07362, 117.07364, 117.07361, 117.0736, 117.07361, 117.07359, 117.073555, 117.07359, 117.07361, 117.07363, 117.07362, 117.07364, 117.07367, 117.07369, 117.07371, 117.07373, 117.0737, 117.0737, 117.07373, 117.07371]
    peak_data_2_3.intensities = [93717.125, 1763907.1, 5752348.5, 15781647.0, 27925880.0, 33619840.0, 45919956.0, 47706240.0, 45536036.0, 47644984.0, 47252076.0, 45883776.0, 38920736.0, 33010866.0, 28096352.0, 25753868.0, 18747672.0, 15042674.0, 11448191.0, 8243860.5, 6194592.5, 3854025.5, 2954004.2, 2723647.0, 2638296.8, 2460238.0, 2393239.0]
    peak_data_2_3.relative_intensities = [93717.125, 1763907.1, 5752348.5, 15781647.0, 27925880.0, 33619840.0, 45919956.0, 47706240.0, 45536036.0, 47644984.0, 47252076.0, 45883776.0, 38920736.0, 33010866.0, 28096352.0, 25753868.0, 18747672.0, 15042674.0, 11448191.0, 8243860.5, 6194592.5, 3854025.5, 2954004.2, 2723647.0, 2638296.8, 2460238.0, 2393239.0]
    peak_data_2_3.pattern_ids = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    peak_data_2_3.measurement_ids = [9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38]

    peakset_2.peaks.append(Peak("masschromatogram", "142", "45.49818801879883", "117.0736635645465", "4.770624E7", "2", None, peak_data_2_3))

    peak_data_2_4 = PeakData("centroid", 27)
    peak_data_2_4.scan_ids = [-3.85186e-34, -1.540744e-33, -6.162976e-33, -2.4651903e-32, -9.8607613e-32, -3.9443045e-31, -1.5777218e-30, -6.3108872e-30, -2.524355e-29, -1.009742e-28, -4.038968e-28, -1.6155871e-27, -6.4623485e-27, -2.5849394e-26, -1.0339758e-25, -4.135903e-25, -1.6543612e-24, -6.617445e-24, -2.646978e-23, -1.0587912e-22, -4.2351647e-22, -1.6940659e-21, -6.7762636e-21, -2.7105054e-20, -1.0842022e-19, -4.3368087e-19, -1.7347235e-18]
    peak_data_2_4.retention_times = [43.281708, 43.58394, 43.8862, 44.188683, 44.490944, 44.793175, 45.095806, 45.3983, 45.701187, 46.0038, 46.30667, 46.609543, 46.912666, 47.215916, 47.519535, 47.823284, 48.12703, 48.4309, 48.734898, 49.039146, 49.343025, 49.64677, 49.950893, 50.255154, 50.560013, 50.86477, 51.170506]
    peak_data_2_4.masses = [117.0741, 117.07407, 117.07404, 117.07396, 117.073875, 117.07382, 117.07377, 117.07374, 117.073715, 117.073685, 117.073654, 117.07367, 117.07366, 117.07365, 117.07365, 117.073685, 117.07367, 117.073715, 117.07367, 117.0737, 117.07371, 117.07375, 117.0737, 117.07375, 117.073814, 117.07409, 117.07407]
    peak_data_2_4.intensities = [526949.2, 2455655.0, 8453453.0, 17311528.0, 31462124.0, 45567556.0, 54622860.0, 51680980.0, 52184784.0, 53566370.0, 53146196.0, 49472468.0, 40819190.0, 35962984.0, 31263728.0, 24212380.0, 21883842.0, 16260801.0, 13257513.0, 9424582.0, 6601539.5, 4694704.5, 2994363.8, 2992259.2, 2652661.2, 2949231.0, 2453833.0]
    peak_data_2_4.relative_intensities = [526949.2, 2455655.0, 8453453.0, 17311528.0, 31462124.0, 45567556.0, 54622860.0, 51680980.0, 52184784.0, 53566370.0, 53146196.0, 49472468.0, 40819190.0, 35962984.0, 31263728.0, 24212380.0, 21883842.0, 16260801.0, 13257513.0, 9424582.0, 6601539.5, 4694704.5, 2994363.8, 2992259.2, 2652661.2, 2949231.0, 2453833.0]
    peak_data_2_4.pattern_ids = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    peak_data_2_4.measurement_ids = [3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37]

    peakset_2.peaks.append(Peak("masschromatogram", "142", "45.09580612182617", "117.07373996569538", "5.462286E7", "3", None, peak_data_2_4))

    peak_data_2_5 = PeakData("centroid", 27)
    peak_data_2_5.scan_ids = [-3.85186e-34, -1.540744e-33, -6.162976e-33, -2.4651903e-32, -9.8607613e-32, -3.9443045e-31, -1.5777218e-30, -6.3108872e-30, -2.524355e-29, -1.009742e-28, -4.038968e-28, -1.6155871e-27, -6.4623485e-27, -2.5849394e-26, -1.0339758e-25, -4.135903e-25, -1.6543612e-24, -6.617445e-24, -2.646978e-23, -1.0587912e-22, -4.2351647e-22, -1.6940659e-21, -6.7762636e-21, -2.7105054e-20, -1.0842022e-19, -4.3368087e-19, -1.7347235e-18]
    peak_data_2_5.retention_times = [43.386734, 43.68873, 43.991104, 44.293358, 44.59585, 44.898228, 45.200844, 45.50322, 45.805965, 46.108345, 46.410847, 46.713844, 47.016594, 47.319714, 47.623215, 47.92671, 48.23046, 48.534325, 48.838455, 49.142445, 49.446323, 49.75007, 50.0542, 50.358315, 50.66294, 50.96781, 51.273804]
    peak_data_2_5.masses = [117.073875, 117.07397, 117.07408, 117.074066, 117.073944, 117.07386, 117.0738, 117.073746, 117.073715, 117.07373, 117.0737, 117.073654, 117.07368, 117.07363, 117.07362, 117.073654, 117.07366, 117.073685, 117.07373, 117.073685, 117.07373, 117.07375, 117.07378, 117.07377, 117.073784, 117.07376, 117.07375]
    peak_data_2_5.intensities = [325591.2, 1309431.9, 5863402.0, 14150168.0, 24853338.0, 37394828.0, 47789180.0, 54633700.0, 57754588.0, 49380200.0, 50046452.0, 46288450.0, 40296532.0, 37437292.0, 31500556.0, 26832052.0, 22455318.0, 16541885.0, 13493258.0, 9530814.0, 7289770.0, 5333646.5, 3256938.8, 2954859.8, 2779103.2, 2491018.0, 2088052.9]
    peak_data_2_5.relative_intensities = [325591.2, 1309431.9, 5863402.0, 14150168.0, 24853338.0, 37394828.0, 47789180.0, 54633700.0, 57754588.0, 49380200.0, 50046452.0, 46288450.0, 40296532.0, 37437292.0, 31500556.0, 26832052.0, 22455318.0, 16541885.0, 13493258.0, 9530814.0, 7289770.0, 5333646.5, 3256938.8, 2954859.8, 2779103.2, 2491018.0, 2088052.9]
    peak_data_2_5.pattern_ids = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    peak_data_2_5.measurement_ids = [1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36]

    peakset_2.peaks.append(Peak("masschromatogram", "144", "45.805965423583984", "117.07374172100248", "5.7754588E7", "4", None, peak_data_2_5))

    #self, type: str, scan: str, retention_time: str, mass: float, intensity: float, measurement_id: str, pattern_id: str, sha1sum: str, signal: str, peak_data: PeakData
    peakset_3 = Peak("peakset","284", "89.37606660709825", "133.1049456966923","8.7058072E7","136","8th7onqkd1UAFzpxcZGyytXRubA=", None, None)

    # self, unit: str = "", ontology_ref: str = "", label: str = "", value: str = "", value_type: str = "STRING"
    peakset_3.add_annotation(Annotation("", None, "codadw", "0.989063788910469", "STRING"))
    peakset_3.add_annotation(Annotation("", None, "id", "146", "STRING"))
    peakset_3.add_annotation(Annotation("", None, "relation.ship", "bp|C13 isotope #1", "STRING"))
    peakset_3.add_annotation(Annotation("", None, "relation.id", "4", "INTEGER"))

    peak_data_3_1 = PeakData("centroid", 14)
    peak_data_3_1.scan_ids = [-6.338253e+29, -4.056482e+31, -6.490371e+32, -2.5961484e+33, -1.0384594e+34, -1.661535e+35, 2.4262203e-35, 3.8819525e-34, 6.211124e-33, 2.4844496e-32, 9.937799e-32, 1.5900478e-30, 1.0420537e-25, 2.7316813e-20]
    peak_data_3_1.retention_times = [81.51453, 82.51439, 83.18439, 83.52076, 83.856895, 84.52913, 88.56522, 89.23349, 89.9016, 90.234856, 90.56721, 91.23597, 93.91306, 96.92292]
    peak_data_3_1.masses = [133.10515, 133.10504, 133.10518, 133.1051, 133.10509, 133.10507, 133.10507, 133.105, 133.10526, 133.10518, 133.10521, 133.10513, 133.10522, 133.10504]
    peak_data_3_1.intensities = [3770.7651, 3961.9734, 3967.2366, 3292.833, 4757.106, 3443.5247, 4079.0386, 3514.9773, 3949.2112, 6411.128, 6716.513, 4616.895, 3029.146, 3182.505]
    peak_data_3_1.relative_intensities = [3770.7651, 3961.9734, 3967.2366, 3292.833, 4757.106, 3443.5247, 4079.0386, 3514.9773, 3949.2112, 6411.128, 6716.513, 4616.895, 3029.146, 3182.505]
    peak_data_3_1.pattern_ids = [None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    peak_data_3_1.measurement_ids = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    peakset_3.peaks.append(Peak("masschromatogram", "268", "90.56720733642578", "133.10514259383442", "6716.51318359375", "0", None, peak_data_3_1))

    peak_data_3_2 = PeakData("centroid", 18)
    peak_data_3_2.scan_ids = [-1.5474251e+26, -6.338253e+29, -2.5353012e+30, -1.0141205e+31, -4.056482e+31, -1.6225928e+32, -2.5961484e+33, -1.7014118e+38, 2.3693558e-38, 3.7909693e-37, 1.5163877e-36, 6.065551e-36, 2.4262203e-35, 9.704881e-35, 6.211124e-33, 2.4844496e-32, 6.669144e-24, 1.067063e-22]
    peak_data_3_2.retention_times = [80.484024, 82.52776, 82.86777, 83.207146, 83.54838, 83.89113, 84.57425, 87.30448, 87.99137, 88.673355, 89.01672, 89.35959, 89.70146, 90.04211, 91.067474, 91.409096, 96.20268, 96.88329]
    peak_data_3_2.masses = [133.10527, 133.10518, 133.10515, 133.10509, 133.10516, 133.10518, 133.10526, 133.1052, 133.10522, 133.10513, 133.10507, 133.10524, 133.10522, 133.10527, 133.10506, 133.10527, 133.10512, 133.10492]
    peak_data_3_2.intensities = [3720.1785, 3720.8628, 5311.803, 3621.4814, 4990.8916, 3916.6465, 2880.921, 3319.9663, 3555.4814, 4822.836, 3684.6519, 2369.4216, 5714.4385, 4989.664, 3956.4663, 4659.307, 3272.1638, 2495.1804]
    peak_data_3_2.relative_intensities = [3720.1785, 3720.8628, 5311.803, 3621.4814, 4990.8916, 3916.6465, 2880.921, 3319.9663, 3555.4814, 4822.836, 3684.6519, 2369.4216, 5714.4385, 4989.664, 3956.4663, 4659.307, 3272.1638, 2495.1804]
    peak_data_3_2.pattern_ids = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    peak_data_3_2.measurement_ids = [2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38, 2.3509887e-38]
    peakset_3.peaks.append(Peak("masschromatogram", "262", "89.70146179199219", "133.10517815048766", "5714.4384765625", "1", None, peak_data_3_2))

    peak_data_3_3 = PeakData("centroid", 61)
    peak_data_3_3.scan_ids = [-1.661535e+35, -6.64614e+35, -2.658456e+36, -1.0633824e+37, -4.2535296e+37, -1.7014118e+38, 9.1835e-41, 2.3693558e-38, 9.477423e-38, 3.7909693e-37, 1.5163877e-36, 6.065551e-36, 2.4262203e-35, 9.704881e-35, 3.8819525e-34, 1.552781e-33, 6.211124e-33, 2.4844496e-32, 9.937799e-32, 3.9751194e-31, 1.5900478e-30, 6.360191e-30, 2.5440764e-29, 1.0176306e-28, 4.0705223e-28, 1.628209e-27, 6.512836e-27, 2.6051343e-26, 1.0420537e-25, 4.168215e-25, 1.667286e-24, 6.669144e-24, 2.6676575e-23, 1.067063e-22, 4.268252e-22, 1.7073008e-21, 6.829203e-21, 2.7316813e-20, 1.0926725e-19, 4.37069e-19, 1.748276e-18, 6.993104e-18, 2.7972416e-17, 1.1188966e-16, 4.4755866e-16, 1.7902346e-15, 7.1609385e-15, 2.8643754e-14, 1.1457502e-13, 4.5830006e-13, 1.8332003e-12, 7.332801e-12, 2.9331204e-11, 1.1732482e-10, 4.6929927e-10, 1.877197e-09, 7.508788e-09, 3.0035153e-08, 1.2014061e-07, 4.8056245e-07, 1.9222498e-06]
    peak_data_3_3.retention_times = [78.62559, 78.93223, 79.239586, 79.54758, 79.85696, 80.165955, 80.47696, 80.78732, 81.09759, 81.40732, 81.71633, 82.02569, 82.33457, 82.64331, 82.951805, 83.25893, 83.56555, 83.871796, 84.17718, 84.48219, 84.78742, 85.092316, 85.397545, 85.702805, 86.00891, 86.31581, 86.62316, 86.93143, 87.239784, 87.54816, 87.85641, 88.165276, 88.47327, 88.78065, 89.08803, 89.39614, 89.7039, 90.01176, 90.32051, 90.62926, 90.939384, 91.250374, 91.5615, 91.873116, 92.185745, 92.49839, 92.81112, 93.123764, 93.435616, 93.74688, 94.055984, 94.36486, 94.67361, 94.98198, 95.28962, 95.59685, 95.90486, 96.21247, 96.520355, 96.829216, 97.13847]
    peak_data_3_3.masses = [133.10493, 133.10504, 133.10497, 133.10506, 133.10506, 133.10504, 133.105, 133.10504, 133.10501, 133.10498, 133.10503, 133.10501, 133.10498, 133.10501, 133.10501, 133.10507, 133.10495, 133.10503, 133.10507, 133.10501, 133.10498, 133.10493, 133.1051, 133.10516, 133.1051, 133.105, 133.10506, 133.10492, 133.10503, 133.10504, 133.10501, 133.10497, 133.105, 133.10503, 133.10501, 133.10498, 133.10504, 133.10501, 133.105, 133.10504, 133.10501, 133.10504, 133.10526, 133.10544, 133.10504, 133.10507, 133.10509, 133.105, 133.10509, 133.10507, 133.1051, 133.10503, 133.10509, 133.10498, 133.10503, 133.10506, 133.10504, 133.1049, 133.10507, 133.10504, 133.10501]
    peak_data_3_3.intensities = [43268.973, 169303.44, 179924.45, 220902.58, 251687.55, 292059.12, 384640.88, 395514.56, 545510.94, 640109.4, 682982.44, 973734.56, 991654.1, 950841.2, 870854.2, 701882.9, 645153.0, 472151.88, 237638.84, 233032.98, 183810.17, 119572.125, 99817.305, 99559.88, 75987.69, 102187.766, 156032.12, 183249.8, 375191.94, 498584.3, 828766.0, 1112978.9, 1667369.4, 1940105.6, 2114710.5, 1910150.1, 1997489.4, 1703247.8, 1517944.5, 1318679.5, 1008359.75, 758946.2, 596235.7, 439125.38, 353807.34, 268649.78, 204270.97, 153789.55, 129111.22, 160218.19, 168977.67, 203124.88, 176021.77, 161010.92, 188254.64, 157588.88, 155889.69, 124876.81, 143726.22, 115967.21, 97029.87]
    peak_data_3_3.relative_intensities = [43268.973, 169303.44, 179924.45, 220902.58, 251687.55, 292059.12, 384640.88, 395514.56, 545510.94, 640109.4, 682982.44, 973734.56, 991654.1, 950841.2, 870854.2, 701882.9, 645153.0, 472151.88, 237638.84, 233032.98, 183810.17, 119572.125, 99817.305, 99559.88, 75987.69, 102187.766, 156032.12, 183249.8, 375191.94, 498584.3, 828766.0, 1112978.9, 1667369.4, 1940105.6, 2114710.5, 1910150.1, 1997489.4, 1703247.8, 1517944.5, 1318679.5, 1008359.75, 758946.2, 596235.7, 439125.38, 353807.34, 268649.78, 204270.97, 153789.55, 129111.22, 160218.19, 168977.67, 203124.88, 176021.77, 161010.92, 188254.64, 157588.88, 155889.69, 124876.81, 143726.22, 115967.21, 97029.87]
    peak_data_3_3.pattern_ids = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    peak_data_3_3.measurement_ids = [9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38, 9.403955e-38]
    peakset_3.peaks.append(Peak("masschromatogram", "284", "89.08802795410156", "133.10502761888637", "2114710.5", "2", None, peak_data_3_3))

    peak_data_3_4 = PeakData("centroid", 62)
    peak_data_3_4.scan_ids = [-6.64614e+35, -2.658456e+36, -1.0633824e+37, -4.2535296e+37, -1.7014118e+38, 9.1835e-41, 2.3693558e-38, 9.477423e-38, 3.7909693e-37, 1.5163877e-36, 6.065551e-36, 2.4262203e-35, 9.704881e-35, 3.8819525e-34, 1.552781e-33, 6.211124e-33, 2.4844496e-32, 9.937799e-32, 3.9751194e-31, 1.5900478e-30, 6.360191e-30, 2.5440764e-29, 1.0176306e-28, 4.0705223e-28, 1.628209e-27, 6.512836e-27, 2.6051343e-26, 1.0420537e-25, 4.168215e-25, 1.667286e-24, 6.669144e-24, 2.6676575e-23, 1.067063e-22, 4.268252e-22, 1.7073008e-21, 6.829203e-21, 2.7316813e-20, 1.0926725e-19, 4.37069e-19, 1.748276e-18, 6.993104e-18, 2.7972416e-17, 1.1188966e-16, 4.4755866e-16, 1.7902346e-15, 7.1609385e-15, 2.8643754e-14, 1.1457502e-13, 4.5830006e-13, 1.8332003e-12, 7.332801e-12, 2.9331204e-11, 1.1732482e-10, 4.6929927e-10, 1.877197e-09, 7.508788e-09, 3.0035153e-08, 1.2014061e-07, 4.8056245e-07, 1.9222498e-06, 7.688999e-06, 3.0755997e-05]
    peak_data_3_4.retention_times = [78.468346, 78.77408, 79.08096, 79.38832, 79.69595, 80.00444, 80.31445, 80.624565, 80.93419, 81.24356, 81.552315, 81.86144, 82.17043, 82.479065, 82.78643, 83.09368, 83.40054, 83.70631, 84.01154, 84.3163, 84.62091, 84.92566, 85.2304, 85.535286, 85.84103, 86.147156, 86.45353, 86.7604, 87.068405, 87.37652, 87.68415, 87.99202, 88.29939, 88.60663, 88.91402, 89.22088, 89.52788, 89.83526, 90.142876, 90.45137, 90.76012, 91.06951, 91.38011, 91.690254, 92.00086, 92.312, 92.622986, 92.93373, 93.244225, 93.55372, 93.86322, 94.17122, 94.47911, 94.78659, 95.0941, 95.40134, 95.70834, 96.01583, 96.32359, 96.63183, 96.94083, 97.25032]
    peak_data_3_4.masses = [133.10493, 133.1051, 133.10518, 133.10504, 133.10512, 133.10513, 133.10507, 133.10512, 133.10506, 133.10507, 133.1051, 133.10506, 133.10503, 133.10504, 133.10507, 133.10503, 133.10504, 133.1051, 133.1051, 133.10509, 133.1051, 133.10506, 133.10516, 133.10492, 133.1049, 133.10498, 133.10506, 133.10509, 133.10507, 133.10506, 133.10506, 133.10504, 133.10507, 133.10503, 133.10504, 133.10504, 133.10506, 133.10509, 133.10507, 133.10507, 133.10506, 133.10509, 133.1051, 133.10509, 133.10509, 133.10516, 133.1051, 133.10509, 133.10513, 133.10512, 133.10516, 133.10513, 133.10506, 133.10516, 133.105, 133.10503, 133.1052, 133.1052, 133.10518, 133.10509, 133.10518, 133.10515]
    peak_data_3_4.intensities = [46569.832, 188357.6, 168627.25, 269857.06, 319089.66, 384434.78, 350413.66, 427658.75, 555702.6, 706515.4, 995949.06, 1007303.9, 955302.5, 930309.4, 946331.94, 726297.5, 521817.97, 334462.84, 268510.66, 223465.86, 152540.28, 146357.22, 165593.56, 56096.67, 36839.254, 102968.695, 158774.73, 265209.06, 442063.25, 680439.56, 1055508.4, 1382072.2, 1884543.5, 2137622.5, 2125802.5, 2446758.2, 2093650.6, 1833380.0, 1560283.0, 1243553.5, 869793.56, 688489.06, 548384.75, 444926.62, 349555.5, 263333.88, 193267.86, 163500.61, 137684.44, 130829.51, 133849.72, 179909.4, 186962.73, 137588.27, 203530.06, 159529.4, 207525.1, 196195.4, 132697.08, 122604.14, 100621.17, 57931.613]
    peak_data_3_4.relative_intensities = [46569.832, 188357.6, 168627.25, 269857.06, 319089.66, 384434.78, 350413.66, 427658.75, 555702.6, 706515.4, 995949.06, 1007303.9, 955302.5, 930309.4, 946331.94, 726297.5, 521817.97, 334462.84, 268510.66, 223465.86, 152540.28, 146357.22, 165593.56, 56096.67, 36839.254, 102968.695, 158774.73, 265209.06, 442063.25, 680439.56, 1055508.4, 1382072.2, 1884543.5, 2137622.5, 2125802.5, 2446758.2, 2093650.6, 1833380.0, 1560283.0, 1243553.5, 869793.56, 688489.06, 548384.75, 444926.62, 349555.5, 263333.88, 193267.86, 163500.61, 137684.44, 130829.51, 133849.72, 179909.4, 186962.73, 137588.27, 203530.06, 159529.4, 207525.1, 196195.4, 132697.08, 122604.14, 100621.17, 57931.613]
    peak_data_3_4.pattern_ids = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    peak_data_3_4.measurement_ids = [3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37, 3.761582e-37]

    peakset_3.peaks.append(Peak("masschromatogram", "286", "89.22087860107422", "133.10507094229638", "2446758.25", "3", None, peak_data_3_4))

    peak_data_3_5 = PeakData("centroid", 63)
    peak_data_3_5.scan_ids =[-1.661535e+35, -6.64614e+35, -2.658456e+36, -1.0633824e+37, -4.2535296e+37, -1.7014118e+38, 9.1835e-41, 2.3693558e-38, 9.477423e-38, 3.7909693e-37, 1.5163877e-36, 6.065551e-36, 2.4262203e-35, 9.704881e-35, 3.8819525e-34, 1.552781e-33, 6.211124e-33, 2.4844496e-32, 9.937799e-32, 3.9751194e-31, 1.5900478e-30, 6.360191e-30, 2.5440764e-29, 1.0176306e-28, 4.0705223e-28, 1.628209e-27, 6.512836e-27, 2.6051343e-26, 1.0420537e-25, 4.168215e-25, 1.667286e-24, 6.669144e-24, 2.6676575e-23, 1.067063e-22, 4.268252e-22, 1.7073008e-21, 6.829203e-21, 2.7316813e-20, 1.0926725e-19, 4.37069e-19, 1.748276e-18, 6.993104e-18, 2.7972416e-17, 1.1188966e-16, 4.4755866e-16, 1.7902346e-15, 7.1609385e-15, 2.8643754e-14, 1.1457502e-13, 4.5830006e-13, 1.8332003e-12, 7.332801e-12, 2.9331204e-11, 1.1732482e-10, 4.6929927e-10, 1.877197e-09, 7.508788e-09, 3.0035153e-08, 1.2014061e-07, 4.8056245e-07, 1.9222498e-06, 7.688999e-06, 3.0755997e-05]
    peak_data_3_5.retention_times = [78.29988, 78.604996, 78.91074, 79.21725, 79.52437, 79.83262, 80.14137, 80.45112, 80.76224, 81.07224, 81.38299, 81.69335, 82.0036, 82.313354, 82.62248, 82.93097, 83.23974, 83.5476, 83.85511, 84.16172, 84.467606, 84.772835, 85.07771, 85.38246, 85.687325, 85.992455, 86.29783, 86.60382, 86.91057, 87.21769, 87.52594, 87.834206, 88.14231, 88.45008, 88.7573, 89.0647, 89.37168, 89.67906, 89.9863, 90.29342, 90.60129, 90.91029, 91.2193, 91.52954, 91.839806, 92.15104, 92.46293, 92.77579, 93.08815, 93.39978, 93.71091, 94.021774, 94.331276, 94.64053, 94.948395, 95.25552, 95.56326, 95.87115, 96.178635, 96.48601, 96.793755, 97.10188, 97.41076]
    peak_data_3_5.masses = [133.10506, 133.10509, 133.10504, 133.10507, 133.10501, 133.10507, 133.10509, 133.10501, 133.10506, 133.10503, 133.10506, 133.10507, 133.10504, 133.10506, 133.1051, 133.10506, 133.10507, 133.10509, 133.10509, 133.10504, 133.10509, 133.10512, 133.10506, 133.10509, 133.10522, 133.10507, 133.1051, 133.10509, 133.10512, 133.10507, 133.10509, 133.1051, 133.1051, 133.10507, 133.10506, 133.10509, 133.10509, 133.10506, 133.10507, 133.10509, 133.10506, 133.10506, 133.10509, 133.10509, 133.10509, 133.10513, 133.1051, 133.10503, 133.10504, 133.10515, 133.10509, 133.10501, 133.10513, 133.10507, 133.10506, 133.10503, 133.10503, 133.10504, 133.10515, 133.10504, 133.10515, 133.1051, 133.1051]
    peak_data_3_5.intensities = [54959.215, 39440.113, 132835.19, 177216.38, 250070.67, 262947.1, 313972.7, 368751.94, 358692.97, 471059.97, 614236.6, 679260.6, 884290.0, 1020497.5, 931322.2, 953033.06, 836597.1, 783057.75, 577982.1, 385532.84, 315672.1, 167573.9, 192353.19, 123419.664, 49711.59, 44332.176, 117301.33, 110415.39, 196256.94, 242520.11, 557328.94, 778817.8, 1139080.0, 1589932.4, 1975151.4, 2110294.0, 2191027.2, 2357809.8, 1843681.1, 1709849.8, 1410370.1, 1154415.5, 955073.94, 597978.7, 480914.9, 371677.72, 279098.34, 214349.39, 190304.56, 127862.98, 139203.84, 134711.23, 167105.5, 143436.94, 206226.6, 175111.38, 160398.56, 202410.17, 153526.2, 168987.75, 111617.28, 124982.36, 168281.98]
    peak_data_3_5.relative_intensities =[54959.215, 39440.113, 132835.19, 177216.38, 250070.67, 262947.1, 313972.7, 368751.94, 358692.97, 471059.97, 614236.6, 679260.6, 884290.0, 1020497.5, 931322.2, 953033.06, 836597.1, 783057.75, 577982.1, 385532.84, 315672.1, 167573.9, 192353.19, 123419.664, 49711.59, 44332.176, 117301.33, 110415.39, 196256.94, 242520.11, 557328.94, 778817.8, 1139080.0, 1589932.4, 1975151.4, 2110294.0, 2191027.2, 2357809.8, 1843681.1, 1709849.8, 1410370.1, 1154415.5, 955073.94, 597978.7, 480914.9, 371677.72, 279098.34, 214349.39, 190304.56, 127862.98, 139203.84, 134711.23, 167105.5, 143436.94, 206226.6, 175111.38, 160398.56, 202410.17, 153526.2, 168987.75, 111617.28, 124982.36, 168281.98]
    peak_data_3_5.pattern_ids = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    peak_data_3_5.measurement_ids = [1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36, 1.5046328e-36]

    peakset_3.peaks.append(Peak("masschromatogram", "287", "89.67906188964844", "133.10507450965298", "2357809.75", "4", None, peak_data_3_5))

    peaks = { "2328bf6a-fa56-49d7-a10a-2f99e717954f" : peakset_1, "05a5c10d-6fa1-435e-8373-72f04bd79a93" : peakset_2, "7c22bb0c-a5a5-4838-9ceb-e35965c8cbe2" :  peakset_3}
    peak_order = ["2328bf6a-fa56-49d7-a10a-2f99e717954f", "05a5c10d-6fa1-435e-8373-72f04bd79a93", "7c22bb0c-a5a5-4838-9ceb-e35965c8cbe2"]

    peakml = PeakML(header, peaks, peak_order)

    return peakml