import 'dart:convert'; // untuk mengimpor pustaka dart:convert pada kode Dart

void main() {
  String jsonString =
      '{"nama": "Budi Martami", "umur":17, "list_bahasa": ["C++", "Python"]}';
  Map<String, dynamic> mhsJson =
      jsonDecode(jsonString); // Mengurai JSON menjadi objek Map
  print(
      "nama: ${mhsJson['nama']}"); // Mencetak nilai properti 'nama' dari objek 'mhsJson'
  print(
      "umur: ${mhsJson['umur']}"); // Mencetak nilai properti 'umur' dari objek 'mhsJson'
  print(
      "skill: ${mhsJson['list_bahasa']}"); // Mencetak nilai properti 'list_bahasa' dari objek 'mhsJson'

  // Mencetak satu-satu nilai dalam properti 'list_bahasa'
  for (String val in mhsJson['list_bahasa']) {
    print(val);
  }

  // Mendefinisikan variabel-variabel dengan nilai yang akan diubah menjadi JSON
  String nama = "Ahmad Aulia";
  int umur = 20;
  List<dynamic> listBahasa = ["php", "js"];

  // Mengubah objek Dart menjadi JSON
  String mhs2json =
      jsonEncode({"nama": nama, "umur": umur, "list_bahasa": listBahasa});
  print(mhs2json); // Mencetak hasil konversi objek menjadi JSON
}
