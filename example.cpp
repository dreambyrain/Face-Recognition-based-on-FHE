#include "seal/seal.h"
#include <iostream>

using namespace std;
using namespace seal;

int main() {
    // ���ö���ʽģ���Ĵ���
    size_t poly_modulus_degree = 8192;
    EncryptionParameters parms(scheme_type::bfv);
    parms.set_poly_modulus_degree(poly_modulus_degree);

    // ����ϵ��ģ��
    parms.set_coeff_modulus(CoeffModulus::BFVDefault(poly_modulus_degree));

    // ��������ģ��
    parms.set_plain_modulus(PlainModulus::Batching(poly_modulus_degree, 20));

    // ���� SEALContext
    auto context = SEALContext(parms);

    // �������Ƿ���Ч
    if (!context.key_context_data()->qualifiers().using_batching) {
        cout << "Batching is not enabled with the given parameters." << endl;
        return 1;
    }

    // ������Կ
    KeyGenerator keygen(context);
    SecretKey secret_key = keygen.secret_key();
    PublicKey public_key;
    keygen.create_public_key(public_key);

    // �������������������ͱ�����
    Encryptor encryptor(context, public_key);
    Decryptor decryptor(context, secret_key);
    BatchEncoder encoder(context);

    // ��������
    vector<uint64_t> plaintext_vector(encoder.slot_count(), 0);
    plaintext_vector[0] = 42; // ���õ�һ���۵�ֵΪ42
    Plaintext plaintext;
    encoder.encode(plaintext_vector, plaintext);

    // ����
    Ciphertext encrypted;
    encryptor.encrypt(plaintext, encrypted);

    cout << "Encryption and batching are successful!" << endl;

    return 0;
}
