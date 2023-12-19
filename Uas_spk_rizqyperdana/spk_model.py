from settings import MEREK_SCALE,DEV_SCALE_reputasi,DEV_SCALE_prosesor,DEV_SCALE_baterai,DEV_SCALE_harga,DEV_SCALE_ukuran_layar

class BaseMethod():

    def __init__(self, data_dict, **setWeight):

        self.dataDict = data_dict

        # 1-7 (Kriteria)
        self.raw_weight = {
            'nama_hp': 3, 
            'reputasi_brand': 3, 
            'processor_antutu': 5, 
            'baterai': 4, 
            'ukuran_layar': 4, 
            'harga': 1
        }

        if setWeight:
            for item in setWeight.items():
                temp1 = setWeight[item[0]] # value int
                temp2 = {v: k for k, v in setWeight.items()}[item[1]] # key str

                setWeight[item[0]] = item[1]
                setWeight[temp2] = temp1

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {c: round(w/total_weight, 2) for c,w in self.raw_weight.items()}

    @property
    def data(self):
        return [{
            'id': smartphone['id'],
            'nama_hp': MEREK_SCALE[smartphone['nama_hp']],
            'reputasi_brand': DEV_SCALE_reputasi[smartphone['reputasi_brand']],
            'processor_antutu': DEV_SCALE_prosesor[smartphone['processor_antutu']],
            'baterai': DEV_SCALE_baterai[smartphone['baterai']],
            'ukuran_layar': DEV_SCALE_ukuran_layar[smartphone['ukuran_layar']],
            'harga': DEV_SCALE_harga[smartphone['harga']]
        } for smartphone in self.dataDict]

    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]
        nama_hp = [] # max
        reputasi_brand = [] # max
        processor_antutu = [] # max
        baterai = [] # max
        ukuran_layar = [] # max
        harga = [] # min
        for data in self.data:
            nama_hp.append(data['nama_hp'])
            reputasi_brand.append(data['reputasi_brand'])
            processor_antutu.append(data['processor_antutu'])
            baterai.append(data['baterai'])
            ukuran_layar.append(data['ukuran_layar'])
            harga.append(data['harga'])

        max_nama_hp = max(nama_hp)
        max_reputasi_brand = max(reputasi_brand)
        max_processor_antutu = max(processor_antutu)
        max_baterai = max(baterai)
        max_ukuran_layar = max(ukuran_layar)
        min_harga = min(harga)

        return [
            {   'id': data['id'],
                'nama_hp': data['nama_hp']/max_nama_hp, # benefit
                'reputasi_brand': data['reputasi_brand']/max_reputasi_brand, # benefit
                'processor_antutu': data['processor_antutu']/max_processor_antutu, # benefit
                'baterai': data['baterai']/max_baterai, # benefit
                'ukuran_layar': data['ukuran_layar']/max_ukuran_layar, # benefit
                'harga': min_harga/data['harga'] # cost
                }
            for data in self.data
        ]
 

class WeightedProduct(BaseMethod):
    def __init__(self, dataDict, setWeight:dict):
        super().__init__(data_dict=dataDict, **setWeight)
    @property
    def calculate(self):
        weight = self.weight
        result = {row['id']:
    round(
        row['nama_hp'] ** weight['nama_hp'] *
        row['reputasi_brand'] ** weight['reputasi_brand'] *
        row['processor_antutu'] ** weight['processor_antutu'] *
        row['baterai'] ** weight['baterai'] *
        row['ukuran_layar'] ** (-weight['ukuran_layar']) *
        row['harga'] ** weight['harga']
        , 2
    )
    for row in self.normalized_data}

        #sorting
        # return result
        return dict(sorted(result.items(), key=lambda x:x[1], reverse=True))