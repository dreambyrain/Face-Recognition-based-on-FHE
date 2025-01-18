#include "seal/seal.h"
#include <iostream>

using namespace std;
using namespace seal;

int main() {
    // 设置多项式模数的次数
    size_t poly_modulus_degree = 8192;
    EncryptionParameters parms(scheme_type::bfv);
    parms.set_poly_modulus_degree(poly_modulus_degree);

    // 设置系数模数
    parms.set_coeff_modulus(CoeffModulus::BFVDefault(poly_modulus_degree));

    // 设置明文模数
    parms.set_plain_modulus(PlainModulus::Batching(poly_modulus_degree, 20));

    // 创建 SEALContext
    auto context = SEALContext(parms);

    // 检查参数是否有效
    if (!context.key_context_data()->qualifiers().using_batching) {
        cout << "Batching is not enabled with the given parameters." << endl;
        return 1;
    }

    // 生成密钥
    KeyGenerator keygen(context);
    SecretKey secret_key = keygen.secret_key();
    PublicKey public_key;
    keygen.create_public_key(public_key);

    // 创建加密器、解密器和编码器
    Encryptor encryptor(context, public_key);
    Decryptor decryptor(context, secret_key);
    BatchEncoder encoder(context);

    // 编码明文
    vector<uint64_t> plaintext_vector(encoder.slot_count(), 0);
    plaintext_vector[0] = 42; // 设置第一个槽的值为42
    Plaintext plaintext;
    encoder.encode(plaintext_vector, plaintext);

    // 加密
    Ciphertext encrypted;
    encryptor.encrypt(plaintext, encrypted);

    cout << "Encryption and batching are successful!" << endl;

    return 0;
}
