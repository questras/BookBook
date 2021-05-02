
package com.example.bookbook;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

import java.util.Random;


@RunWith(MockitoJUnitRunner.class)
public class SignUpTest {

    @Test
    public void test() {

        SignUp signUp = new SignUp();

        for (int i = 0; i < 100; i++) {
            Random r = new Random();
            int x = r.nextInt(15);

            char[] text = new char[x];

            for (int j = 0; j < x; j++) {

                int y = r.nextInt('~' - '!') + '!';
                text[j] = (char)(y + '0');
            }

            if (x < 8) {
                assert (!signUp.isPasswordValid(String.valueOf(text)));
            } else {
                assert(signUp.isPasswordValid(String.valueOf(text)));
            }
        }

        for (int i = 0; i < 100; i++) {
            Random r = new Random();
            int x = r.nextInt(15) + 10;

            char[] text = new char[x];
            char[] text2 = new char[x];

            boolean same = r.nextBoolean();

            for (int j = 0; j < x; j++) {

                int y = r.nextInt('~' - '!') + '!';
                text[j] = (char)(y + '0');
            }


            if (same) {
                text2 = text;
            }
            else {
                for (int j = 0; j < x; j++) {

                    int y = r.nextInt('~' - '!') + '!';
                    text2[j] = (char)(y + '0');
                }

                if (text == text2) {
                    text2[0]++;
                }
            }

            if (same) {
                assert (signUp.isPasswordSame(String.valueOf(text), String.valueOf(text2)));
            } else {
                assert (!signUp.isPasswordSame(String.valueOf(text), String.valueOf(text2)));
            }
        }

    }
}