import com.nulabinc.zxcvbn.Strength;
import com.nulabinc.zxcvbn.Zxcvbn;

class ZxcvbnDemo{
    public static void main(String[] args){
        System.out.println("This program performs zxcvbn password strength estimation on the given password");
        if(args.length != 1){
            System.out.println("Usage: ./zxcvbn PASSWORD");
            System.exit(0);
        }


        Zxcvbn zxcvbn = new Zxcvbn();

        long startTime = System.nanoTime();
        Strength strength = zxcvbn.measure(args[0]);
        long endTime = System.nanoTime();

        Integer score = strength.getScore();

        StringBuilder resultString = new StringBuilder("The password '");
        resultString.append(args[0]).append("' has score ").append(score.toString());
        resultString.append(" (estimated in ").append((endTime - startTime)/1000000000.0).append(" seconds)");
        System.out.println(resultString.toString());
    }
}
