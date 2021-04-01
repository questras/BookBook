package com.example.bookbook;

import android.os.Bundle;
import android.text.Editable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;

public class SignIn extends Fragment {

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_sign_in, container, false);
        final TextInputLayout passwordTextInput = view.findViewById(R.id.password_text_input);
        final TextInputEditText passwordEditText = view.findViewById(R.id.password_edit_text);
        MaterialButton signUpButton = view.findViewById(R.id.sign_up_button);
        MaterialButton signInButton = view.findViewById(R.id.sign_in_button);

        passwordEditText.setOnKeyListener((v, i, keyEvent) -> {
            if (isPasswordValid(passwordEditText.getText())) {
                passwordTextInput.setError(null);
            }
            return false;
        });

        signInButton.setOnClickListener(v -> {
            if (!isPasswordValid(passwordEditText.getText())) {
                passwordTextInput.setError(getString(R.string.error_password_len));
            } else {
                passwordTextInput.setError(null);
                if (getActivity() != null) {
                    ((WelcomeActivity) getActivity()).switchToMain();
                }
            }
        });

        signUpButton.setOnClickListener(v -> {
            passwordTextInput.setError(null);
            if (getActivity() != null) {
                ((NavigationHost) getActivity()).navigateTo(new SignUp(), true);
            }
        });

        return view;
    }

    private boolean isPasswordValid(@Nullable Editable text) {
        return text != null && text.length() >= 8;
    }
}