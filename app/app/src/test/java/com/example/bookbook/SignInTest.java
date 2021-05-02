
package com.example.bookbook;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

import java.util.Random;


@RunWith(MockitoJUnitRunner.class)
public class SignInTest {

    @Test
    public void test() {

        SignIn signIn = new SignIn();

        for (int i = 0; i < 100; i++) {
            Random r = new Random();
            int x = r.nextInt(15);

            char[] text = new char[x];

            for (int j = 0; j < x; j++) {

                int y = r.nextInt('~' - '!') + '!';
                text[j] = ((char)(y + '0'));

            }

            if (x < 8) {
                assert (!signIn.isPasswordValid(String.valueOf(text)));
            } else {
                assert(signIn.isPasswordValid(String.valueOf(text)));
            }
        }

        for (int i = 0; i < 100; i++) {
            Random r = new Random();
            int x = r.nextInt(15) + 10;

            char[] text = new char[x];


            boolean mail = r.nextBoolean();
            int w = r.nextInt(x);

            for (int j = 0; j < x; j++) {

                if (w == j && mail) {
                    text[j] = '@';
                }
                else {

                    int y = r.nextInt('~' - '!') + '!';
                    if (y == '@') {
                        y++;
                    }
                    text[j] = ((char) (y + '0'));
                }
            }

            if (mail) {
                assert (signIn.isMailValid(String.valueOf(text)));
            } else {
                assert (!signIn.isMailValid(String.valueOf(text)));
            }
        }
    }
}