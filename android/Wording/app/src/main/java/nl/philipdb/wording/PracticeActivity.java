package nl.philipdb.wording;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.KeyEvent;
import android.view.View;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.Arrays;

public class PracticeActivity extends AppCompatActivity {

    private List mList;
    private int mAskedLanguage; // 1 = language 1 | 2 = language 2 | 0 = both
    private boolean mCaseSensitive = true;
    private ArrayList<String> mUsedWords = new ArrayList<>();
    private String[] mRandomWord = new String[2];

    private EditText mTranslation;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_practice);
        // Setup Toolbar
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        // Setup button actions
        mTranslation = (EditText) findViewById(R.id.translation);
        mTranslation.setOnEditorActionListener(new TextView.OnEditorActionListener() {
            @Override
            public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
                if (actionId == R.id.next_word || actionId == EditorInfo.IME_ACTION_GO) {
                    checkWord();
                    return true;
                }
                return false;
            }
        });
        findViewById(R.id.next_word).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                checkWord();
            }
        });

        // Load intent extras
        Intent intent = getIntent();
        mList = (List) intent.getSerializableExtra("list");
        mAskedLanguage = intent.getIntExtra("askedLanguage", 1);
        mCaseSensitive = intent.getBooleanExtra("caseSensitive", true);

        // Set asked language
        if (mAskedLanguage != 0) {
            if (mAskedLanguage == 1) ((TextView) findViewById(R.id.language)).setText(List.getLanguageName(mList.mLanguage1));
            else if (mAskedLanguage == 2) ((TextView) findViewById(R.id.language)).setText(List.getLanguageName(mList.mLanguage2));
        }
        nextWord();
    }

    private void nextWord() {
        // Check if list is done
        if (mUsedWords.size() == mList.mLanguage1Words.size()) {
            // TODO: Show results
        }

        int randomIndexInt = (int) Math.floor(Math.random() * mList.mLanguage1Words.size());
        mRandomWord = new String[]{mList.mLanguage1Words.get(randomIndexInt), mList.mLanguage2Words.get(randomIndexInt)};
        // Check if word is already used
        if (mUsedWords.indexOf(mRandomWord[0]) > -1) nextWord();
        else mUsedWords.add(mRandomWord[0]);

        // Display
        if (mAskedLanguage != 0 && mAskedLanguage <= 2) {
            ((TextView) findViewById(R.id.word_to_translate)).setText(mRandomWord[mAskedLanguage - 1]);
        }
    }

    private void checkWord() {
        if (mAskedLanguage == 1 || mAskedLanguage == 2) {
            if (isInputRight(mTranslation.getText().toString(), mRandomWord[mAskedLanguage == 1 ? 1 : 0])) {
                mTranslation.setText("");
                nextWord();
            } else {
                // TODO: Create function for wrong word
            }
        }
    }

    private boolean isInputRight(String input, String correctWord) {
        // Check for case sensitivity
        if (!mCaseSensitive) {
            input = input.toLowerCase();
            correctWord = correctWord.toLowerCase();
        }

        // Check if the word is right
        if (input.equals(correctWord)) {
            return true;
        } else if (correctWord.split("\\s*[,|/|;]\\s*").length >= 2) {
            String[] inputWordArray = input.split("\\s*[,|/|;]\\s*");
            String[] correctWordArray = correctWord.split("\\s*[,|/|;]\\s*");
            Arrays.sort(inputWordArray);
            Arrays.sort(correctWordArray);

            for (int i = 0; i < inputWordArray.length; i++) {
                if (!inputWordArray[i].equals(correctWordArray[i])) {
                    return false;
                }
            }

            return true;
        } else return false;
    }

}
