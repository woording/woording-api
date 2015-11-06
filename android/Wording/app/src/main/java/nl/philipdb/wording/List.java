package nl.philipdb.wording;

import android.content.res.Resources;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;

public class List implements Serializable {
    public String mName;
    public String mLanguage1;
    public String mLanguage2;
    public String mSharedWith;

    public ArrayList<String> mLanguage1Words;
    public ArrayList<String> mLanguage2Words;

    public List(String n, String l1, String l2, String sw) {
        mName = n;
        mLanguage1 = l1;
        mLanguage2 = l2;
        mSharedWith = sw;
    }

    public void setWords(ArrayList<String> language1, ArrayList<String> language2) {
        if (language1.size() == language2.size()) {
            mLanguage1Words = language1;
            mLanguage2Words = language2;
        }
    }

    public String getTranslation(String word) {
        if (mLanguage1Words.contains(word)) return mLanguage2Words.get(mLanguage1Words.indexOf(word));
        else if (mLanguage2Words.contains(word)) return mLanguage1Words.get(mLanguage1Words.indexOf(word));
        else return null;
    }

    public static String getLanguageName(String languageCode) {
        Resources res = MainActivity.mContext.getResources();
        ArrayList<String> codes = new ArrayList<>(Arrays.asList(res.getStringArray(R.array.language_codes)));
        ArrayList<String> languages = new ArrayList<>(Arrays.asList(res.getStringArray(R.array.languages)));

        return languages.get(codes.indexOf(languageCode));
    }

    public int getTotalWords() {
        return mLanguage1Words.size();
    }
}
