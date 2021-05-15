package pl.mimuw.bookbook.ui;

import android.graphics.Bitmap;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import pl.mimuw.bookbook.R;
import pl.mimuw.bookbook.db.main.MainViewModel;
import pl.mimuw.bookbook.db.main.Offer;

public class OfferInfo extends Fragment {

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_offer_info, container, false);
        MainViewModel model = new ViewModelProvider(requireActivity()).get(MainViewModel.class);
        int position = getArguments().getInt("position");
        Offer thisOffer = model.getOffers().get(position);
        ((TextView) view.findViewById(R.id.title)).setText(thisOffer.getTitle());
        ((TextView) view.findViewById(R.id.author)).setText(thisOffer.getAuthor());
        ((TextView) view.findViewById(R.id.description_text)).setText(thisOffer.getDescription());
        ((TextView) view.findViewById(R.id.state_text)).setText(thisOffer.getState());
        ((TextView) view.findViewById(R.id.city_text)).setText(thisOffer.getCity());
        ((TextView) view.findViewById(R.id.phone_number_text)).setText(thisOffer.getLenderPhone());
        ((TextView) view.findViewById(R.id.email_text)).setText(thisOffer.getLenderEmail());
        if (model.getOffersImages().containsKey(position)) {
            ((ImageView) view.findViewById(R.id.book_image)).
                    setImageBitmap((Bitmap.createScaledBitmap(model.getOffersImages().
                            get(position), 500, 500, true)));
        }

        return view;
    }
}