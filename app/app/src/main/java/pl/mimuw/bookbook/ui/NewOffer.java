package pl.mimuw.bookbook.ui;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;

import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;

import org.json.JSONObject;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;

import pl.mimuw.bookbook.R;
import pl.mimuw.bookbook.db.main.MainViewModel;

public class NewOffer extends Fragment {

    public static final int REQUEST_IMAGE_CAPTURE = 1;
    private ImageButton addPhotoButton;
    private File[] imageToSend;

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_new_offer, container, false);
        imageToSend = new File[]{null};
        MaterialButton addOfferButton = view.findViewById(R.id.add_offer_button);
        addPhotoButton = view.findViewById(R.id.add_photo_button);
        MainViewModel model = new ViewModelProvider(requireActivity()).get(MainViewModel.class);
        model.getAddOfferResp().observe(requireActivity(), new AddOfferResponseObserver(view, imageToSend));

        addOfferButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                model.addOffer(((TextInputEditText) view.findViewById(R.id.book_title_edit_text)).getText().toString(),
                        ((TextInputEditText) view.findViewById(R.id.book_author_edit_text)).getText().toString(),
                        ((TextInputEditText) view.findViewById(R.id.description_edit_text)).getText().toString(),
                        ((TextInputEditText) view.findViewById(R.id.state_edit_text)).getText().toString(),
                        ((TextInputEditText) view.findViewById(R.id.city_edit_text)).getText().toString(),
                        ((TextInputEditText) view.findViewById(R.id.phone_edit_text)).getText().toString());
            }
        });

        addPhotoButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                if (takePictureIntent.resolveActivity(requireActivity().getPackageManager()) != null) {
                    startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
                }
            }
        });

        return view;
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == -1) {
            Bundle extras = data.getExtras();
            Bitmap offerImageToDisplay = (Bitmap) extras.get("data");
            addPhotoButton.setImageBitmap(Bitmap.createScaledBitmap(offerImageToDisplay,
                    500, 500, true));
            try {
                imageToSend[0] = createImageFile(offerImageToDisplay);
            } catch (IOException e) {
                Log.e(getClass().getSimpleName(), "Error writing to file", e);
                imageToSend[0] = null;
            }
        }
    }

    private File createImageFile(Bitmap bitmap) throws IOException {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "JPEG_" + timeStamp + "_";
        File storageDir = requireActivity().getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(
                imageFileName,  /* prefix */
                ".jpg",   /* suffix */
                storageDir      /* directory */
        );
        OutputStream os;
        try {
            os = new FileOutputStream(image);
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, os);
            os.flush();
            os.close();
        } catch (Exception e) {
            Log.e(getClass().getSimpleName(), "Error writing bitmap", e);
        }
        return image;
    }

    class AddOfferResponseObserver implements Observer<JSONObject> {
        private final ArrayList<TextInputLayout> textFields;
        private final ArrayList<String> fieldNames = new ArrayList<String>(
                Arrays.asList("title", "author", "description", "state", "city", "lender_phone"));
        private final File[] toSend;

        public AddOfferResponseObserver(View view, File[] image) {
            textFields = new ArrayList<>();
            textFields.add(view.findViewById(R.id.book_title_text_input));
            textFields.add(view.findViewById(R.id.book_author_text_input));
            textFields.add(view.findViewById(R.id.state_text_input));
            textFields.add(view.findViewById(R.id.city_text_input));
            textFields.add(view.findViewById(R.id.description_text_input));
            textFields.add(view.findViewById(R.id.phone_text_input));
            toSend = image;
        }

        @Override
        public void onChanged(JSONObject response) {
            if (response != null && !response.has("id")) {
                for (int i = 0; i < fieldNames.size(); i++) {
                    if (response.has(fieldNames.get(i))) {
                        textFields.get(i).setError(response.optJSONArray(fieldNames.get(i)).optString(0));
                    } else
                        textFields.get(i).setError(null);
                }
            }

            if (response != null && response.has("id") && toSend[0] != null) {
                new ViewModelProvider(requireActivity()).get(MainViewModel.class).addImage(
                        response.optInt("id"), toSend[0], new MutableLiveData<>());
                toSend[0] = null;
            }
        }
    }

}
