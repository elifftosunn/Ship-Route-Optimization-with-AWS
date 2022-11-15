## Ship Route Optimization with AWS

3 dakikada bir websitesinden çektiğimiz dataları EC2 ile S3 bucket'a yolladık. Daha sonra RDS üzerinde sql sorguları ile Tanker ve Cargo gemilerini çekerek veri temizleme, veri önişleme aşamalarından sonra KNN ve Random Forest Regressor algoritmaları ile SageMaker'da train ettik. SageMaker'da predict edilen data S3 bucket'a geri atıldı ve daha sonra lambda fonksiyonu ile S3 Bucket trigger oluşturduk ve verileri RDS'e insert ettik. Statik websitesi oluşturup S3 bucket'a yükledik ve yayınladık. RDS'teki verileri alabilmek için de bir lambda fonksiyonu yazdık. RDS'teki verileri alıp statik websitesinde gösterimini yaptık. Böylece Cargo ve Tanker gemileri için bir rota optimizasyonu oluşturmuş olduk. 

![aws](https://user-images.githubusercontent.com/92747017/202001018-0b23d5ef-034e-4453-8cd7-862334ef4f3d.PNG)


![aws2](https://user-images.githubusercontent.com/92747017/202001034-5880ff89-170e-4309-b73c-50fe86e93fe4.PNG)












