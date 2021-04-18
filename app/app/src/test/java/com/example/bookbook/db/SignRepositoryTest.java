package com.example.bookbook.db;

import android.util.Pair;

import androidx.lifecycle.MutableLiveData;

import org.json.JSONObject;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;
import androidx.arch.core.executor.testing.InstantTaskExecutorRule;

import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.Assert.assertTrue;

@RunWith(JUnit4.class)
public class SignRepositoryTest {

    @Rule
    public InstantTaskExecutorRule instantTaskExecutorRule = new InstantTaskExecutorRule();

    private final String alphaNumericChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            + "0123456789"
            + "abcdefghijklmnopqrstuvxyz";
    private final String specialChars = "!@#$%^&*()_+";

    @Test
    public void authenticateValidData() throws InterruptedException, BrokenBarrierException {
        AtomicInteger counter = new AtomicInteger();
        CyclicBarrier barrier = new CyclicBarrier(2);
        SignRepository repo = SignRepository.getInstance();
        MutableLiveData<Pair<ResponseToken, JSONObject>> data = new MutableLiveData<>();
        data.observeForever(response -> {
            assertTrue(response.first != null || response.second.has("non_field_errors"));
            if (counter.incrementAndGet() == 2) {
                try {
                    barrier.await();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });
        for (int i = 0; i < 1; i++) {
            repo.authenticate(generateValidEmail(), generateValidPassword(), data);
        }
        barrier.await();
    }

    private String generateValidEmail() {
        StringBuilder email = new StringBuilder();
        int prefixSizeRand = ThreadLocalRandom.current().nextInt(1, 30);
        for (int i = 0; i < prefixSizeRand; i++) {
            email.append(alphaNumericChars.charAt((int) (alphaNumericChars.length() * Math.random())));
        }
        email.append("@gm.com");
        return email.toString();
    }

    private String generateValidPassword() {
        StringBuilder pass = new StringBuilder();
        int alphaNumericRand = ThreadLocalRandom.current().nextInt(5, 10);
        int specialRand = ThreadLocalRandom.current().nextInt(5, 10);
        for (int i = 0; i < alphaNumericRand; i++) {
            pass.append(alphaNumericChars.charAt((int) (alphaNumericChars.length() * Math.random())));
        }
        for (int i = 0; i < specialRand; i++) {
            pass.append(specialChars.charAt((int) (specialChars.length() * Math.random())));
        }
        return pass.toString();
    }
}
