package pl.mimuw.bookbook.ui;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import android.text.Editable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;

import pl.mimuw.bookbook.R;

import pl.mimuw.bookbook.db.sign.SignViewModel;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;

public class SignUp extends Fragment {

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_sign_up, container, false);
        final TextInputLayout passwordTextInput = view.findViewById(R.id.password_text_input);
        final TextInputLayout retypePasswordTextInput = view.findViewById(R.id.retype_password_text_input);
        final TextInputLayout mailTextInput = view.findViewById(R.id.mail_text_input);
        final TextInputLayout firstNameTextInput = view.findViewById(R.id.first_name_text_input);
        final TextInputLayout lastNameTextInput = view.findViewById(R.id.last_name_text_input);
        final TextInputEditText passwordEditText = view.findViewById(R.id.password_edit_text);
        final TextInputEditText retypePasswordEditText = view.findViewById(R.id.retype_password_edit_text);
        MaterialButton signUpButton = view.findViewById(R.id.add_offer_button);

        SignViewModel model = new ViewModelProvider(requireActivity()).get(SignViewModel.class);
        model.getRegisterResp().observe(requireActivity(), response -> {
//            Wrong credentials handling
            if (response != null) {
                if (response.has("email"))
                    mailTextInput.setError(response.optJSONArray("email").optString(0));
                else
                    mailTextInput.setError(null);

                if (response.has("first_name"))
                    firstNameTextInput.setError(response.optJSONArray("first_name").optString(0));
                else
                    firstNameTextInput.setError(null);

                if (response.has("last_name"))
                    lastNameTextInput.setError(response.optJSONArray("last_name").optString(0));
                else
                    lastNameTextInput.setError(null);

                if (response.has("password"))
                    passwordTextInput.setError(response.optJSONArray("password").optString(0));
                else if (response.has("non_field_errors"))
                    passwordTextInput.setError("Wrong password or mail");
                else
                    passwordTextInput.setError(null);
            }
        });

        passwordEditText.setOnKeyListener((v, i, keyEvent) -> {
            if (isPasswordValid(passwordEditText.getText()))
                passwordTextInput.setError(null);
            if (isPasswordSame(retypePasswordEditText, passwordEditText))
                retypePasswordTextInput.setError(null);
            return false;
        });

        retypePasswordEditText.setOnKeyListener((v, i, keyEvent) -> {
            if (isPasswordSame(retypePasswordEditText, passwordEditText))
                retypePasswordTextInput.setError(null);
            return false;
        });

        signUpButton.setOnClickListener(v -> {
            if (!isPasswordValid(passwordEditText.getText())) {
                passwordTextInput.setError(getString(R.string.error_password_len));
            } else if (!isPasswordSame(retypePasswordEditText, passwordEditText)) {
                retypePasswordTextInput.setError(getString(R.string.error_password_same));
            } else {
                model.register(mailTextInput.getEditText().getText().toString(),
                        passwordEditText.getText().toString(),
                        firstNameTextInput.getEditText().getText().toString(),
                        lastNameTextInput.getEditText().getText().toString());
            }
        });

        return view;
    }

    private boolean isPasswordValid(@Nullable Editable text) {
        return text != null && text.length() >= 8;
    }

    private boolean isPasswordSame(EditText text1, EditText text2) {
        return text1.getText().toString().compareTo(text2.getText().toString()) == 0;
    }
}