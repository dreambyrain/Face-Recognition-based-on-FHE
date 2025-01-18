#include "seal/seal.h"
#include <fstream>
#include <iostream>

using namespace std;
using namespace seal;

void encrypt_and_save(const string &input_file, const string &output_file)
{
    // 1. 设置 CKKS 加密参数
    EncryptionParameters parms(scheme_type::ckks);
    parms.set_poly_modulus_degree(8192); // 通常使用 8192 或更高的值
    parms.set_coeff_modulus(CoeffModulus::Create(8192, { 40, 40, 40, 40 })); // 设置系数模数

    // 2. 创建 SEALContext
    SEALContext context(parms); // 不使用 std::shared_ptr

    // 3. 创建密钥和加密器
    KeyGenerator keygen(context);
    auto secret_key = keygen.secret_key();
    PublicKey public_key;
    keygen.create_public_key(public_key);

    Encryptor encryptor(context, public_key);
    Evaluator evaluator(context);
    Decryptor decryptor(context, secret_key);

    // 4. 加载数据（示例为从 input_file 读取数据）
    ifstream input(input_file);
    if (!input.is_open())
    {
        cerr << "无法打开输入文件: " << input_file << endl;
        return;
    }
    vector<double> data;
    double value;
    while (input >> value)
    {
        data.push_back(value);
    }
    input.close();

    // 5. 编码数据
    CKKSEncoder encoder(context);
    Plaintext plain;
    encoder.encode(data, pow(2.0, 40), plain); // 40-bit 精度

    // 6. 加密数据
    Ciphertext encrypted;
    encryptor.encrypt(plain, encrypted);

    // 7. 保存加密数据到输出文件
    ofstream output(output_file, ios::binary);
    if (!output.is_open())
    {
        cerr << "无法打开输出文件: " << output_file << endl;
        return;
    }
    encrypted.save(output);
    output.close();

    cout << "加密数据已保存到: " << output_file << endl;
}

int main()
{
    const string input_file = "processed_data.yaml"; // 替换为您的输入文件路径
    const string output_file = "encrypted_data.bin"; // 替换为输出文件路径

    encrypt_and_save(input_file, output_file);

    return 0;
}

