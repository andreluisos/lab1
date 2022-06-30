import numpy

jam = [0.009918, 0.007641, 0.010784, 0.014108, 0.008573, 0.008241, 0.005581, 0.005406, 0.005418, 0.005187, 0.004736,
       0.004469, 0.005471, 0.00462,
       0.0048, 0.004713, 0.00377, 0.004964, 0.004611, 0.004017, 0.004496, 0.003506, 0.003785, 0.003666, 0.003459,
       0.003838, 0.002835, 0.004194,
       0.004016, 0.004297, 0.003927, 0.004913, 0.00591, 0.004097, 0.005386, 0.004399, 0.004454, 0.005063, 0.00364,
       0.004228, 0.004829, 0.004573,
       0.004052, 0.005128, 0.004953, 0.004426, 0.005241, 0.005116, 0.006084, 0.007356, 0.006592, 0.006257, 0.00666,
       0.007127, 0.006642, 0.007944,
       0.006514, 0.005838, 0.005687, 0.004246, 0.004369, 0.003749, 0.002925, 0.004248, 0.003342, 0.004016, 0.004231,
       0.004423, 0.004476, 0.004198,
       0.003576, 0.003615, 0.004872, 0.00435, 0.00343, 0.005107, 0.004474, 0.004999, 0.005466, 0.005047, 0.00594,
       0.005109, 0.004571, 0.0044, 0.00474,
       0.004797, 0.003193, 0.004544, 0.003323, 0.004358, 0.004408, 0.004221, 0.004908, 0.003991, 0.004345, 0.003751,
       0.003992, 0.00466, 0.003189,
       0.004346, 0.003741, 0.004159, 0.003422, 0.003938, 0.003935, 0.002819, 0.003611, 0.003057, 0.003107, 0.003478,
       0.002709, 0.002876, 0.003423,
       0.003204, 0.003615, 0.004384, 0.004044, 0.004441, 0.004978, 0.004088, 0.00462, 0.00431, 0.002918, 0.003907,
       0.002921, 0.002916, 0.003123,
       0.003519, 0.002663, 0.002466, 0.002466, 0.002466, 0.003, 0.002466, 0.002466, 0.00326, 0.002466, 0.002977,
       0.003056, 0.00362, 0.003377, 0.003169,
       0.002939, 0.002803, 0.003875, 0.003183, 0.002991, 0.003681, 0.002836, 0.00404, 0.003583, 0.003698, 0.004547,
       0.003471, 0.003087, 0.003112,
       0.003405, 0.003332, 0.002466, 0.003536, 0.002693, 0.002935, 0.002466, 0.00261, 0.002589, 0.002466, 0.002466,
       0.002466, 0.002466, 0.002466,
       0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002675, 0.002466, 0.002545, 0.003388, 0.002673, 0.002961,
       0.003595, 0.003004, 0.002732,
       0.002926, 0.003071, 0.002932, 0.003522, 0.003069, 0.003341, 0.003506, 0.00295, 0.003521, 0.003346, 0.002634,
       0.003765, 0.003542, 0.003622,
       0.004283, 0.004776, 0.004337, 0.00439, 0.00426, 0.003766, 0.004721, 0.003789, 0.003425, 0.004639, 0.003773,
       0.004003, 0.004514, 0.004091,
       0.005017, 0.004045, 0.004071, 0.003897, 0.004319, 0.00417, 0.002769, 0.003989, 0.002466, 0.003232, 0.003003,
       0.00309, 0.002976, 0.002466,
       0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466,
       0.002466, 0.002466, 0.002466,
       0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466,
       0.002466, 0.002466, 0.002466,
       0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466, 0.002466,
       0.002466, 0.002466, 0.002466]

inpc = [0.65, 1.29, 1.28, 0.47, 0.05, 0.07, 0.74, 0.55, 0.39, 0.96, 0.94, 0.74, 0.61, 0.05, 0.13, 0.09, -0.05, 0.3,
        1.39, 1.21, 0.43, 0.16, 0.29, 0.55,
        0.77, 0.49, 0.48, 0.84, 0.57, 0.6, 1.11, 0.79, 0.44, 0.94, 1.29, 0.74, 1.07, 0.31, 0.62, 0.68, 0.09, 0.61, 1.15,
        0.86, 0.83, 1.57, 3.39, 2.7,
        2.47, 1.46, 1.37, 1.38, 0.99, -0.06, 0.04, 0.18, 0.82, 0.39, 0.37, 0.54, 0.83, 0.39, 0.57, 0.41, 0.4, 0.5, 0.73,
        0.5, 0.17, 0.17, 0.44, 0.86,
        0.57, 0.44, 0.73, 0.91, 0.7, -0.11, 0.03, numpy.nan, 0.15, 0.58, 0.54, 0.4, 0.38, 0.23, 0.27, 0.12, 0.13, -0.07,
        0.11, -0.02, 0.16, 0.43, 0.42,
        0.62, 0.49, 0.42, 0.44, 0.26, 0.26, 0.31, 0.32, 0.59, 0.25, 0.3, 0.43, 0.97, 0.69, 0.48, 0.51, 0.64, 0.96, 0.91,
        0.58, 0.21, 0.15, 0.5, 0.38,
        0.29, 0.64, 0.31, 0.2, 0.55, 0.6, 0.42, 0.23, 0.08, 0.16, 0.24, 0.37, 0.24, 0.88, 0.7, 0.71, 0.73, 0.43, -0.11,
        -0.07, -0.07, 0.54, 0.92, 1.03,
        0.6, 0.94, 0.54, 0.66, 0.72, 0.57, 0.22, numpy.nan, 0.42, 0.45, 0.32, 0.57, 0.51, 0.51, 0.39, 0.18, 0.64, 0.55,
        0.26, 0.43, 0.45, 0.63, 0.71,
        0.54, 0.74, 0.92, 0.52, 0.6, 0.59, 0.35, 0.28, -0.13, 0.16, 0.27, 0.61, 0.54, 0.72, 0.63, 0.64, 0.82, 0.78, 0.6,
        0.26, 0.13, 0.18, 0.49, 0.38,
        0.53, 0.62, 1.48, 1.16, 1.51, 0.71, 0.99, 0.77, 0.58, 0.25, 0.51, 0.77, 1.11, 0.9, 1.51, 0.95, 0.44, 0.64, 0.98,
        0.47, 0.64, 0.31, 0.08, 0.17,
        0.07, 0.14, 0.42, 0.24, 0.32, 0.08, 0.36, -0.3, 0.17, -0.03, -0.02, 0.37, 0.18, 0.26, 0.23, 0.18, 0.07, 0.21,
        0.43, 1.43, 0.25, numpy.nan, 0.3,
        0.4, -0.25, 0.14, 0.36, 0.54, 0.77, 0.6, 0.15, 0.01, 0.1, 0.12, -0.05, 0.04, 0.54, 1.22, 0.19, 0.17, 0.18,
        -0.23, -0.25, 0.3, 0.44, 0.36, 0.87,
        0.89, 0.95, 1.46, 0.27, 0.82, 0.86, 0.38]

juros = [0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627,
         0.00246627, 0.00246627, 0.00246627, 0.00246627]

coord_nome = ['180, 795, 380, 775']
coord_ctps = ['25, 680, 150, 650']
coord_pis_pasep = ['370, 727, 480, 695']
coord_empregador = ['25, 730, 185, 680']
coord_empregador_num = ['205, 680, 340, 650']
coord_conta_num = ['375, 680, 585, 650']
coord_juros = ['200, 590, 300, 560']
coords = coord_nome + coord_ctps + coord_pis_pasep + coord_empregador + coord_empregador_num + coord_conta_num + coord_juros

html = """<!DOCTYPE html>
<html lang="pt_br">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
    <body>
        <h2>DADOS DO AUTOR</h2>
        <strong>Nome</strong> <div id="nome">{{nome}}</div><br>
        <strong>PIS/PASEP</strong> <div id="pis_pasep">{{pis_pasep}}</div><br>
        <hr>
        <h2>DADOS DA CONTA FGTS</h2>
        <strong>Empregador</strong> <div id="empregador">{{empregador}}</div><br>
        <strong>Número da conta FGTS</strong> <div id="conta_num">{{conta_num}}</div><br>
        <strong>Taxa de juros</strong> <div id="taxa_juros">{{taxa_juros}}</div><br>
        <hr>
        <h2>PLANILHA COM CORREÇÃO</h2>
        <div id="planilha"></div>
        <hr>
        <h2>TOTAL DEVIDO</h2>
        <strong>Total devido para esta conta</strong> <div id="total_devido">{{total_devido}}</div><br>
    </body>
</html>"""
