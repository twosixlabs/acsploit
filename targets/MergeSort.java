import java.util.Arrays;

class MergeSort{

	public static Integer comparisons = 0;

	public static int[] sort(int[] array){
		if(array.length == 1){  // return arrays of length 1 as definitionally sorted
			return array;
		} else if (array.length == 2){  // trivially sort arrays of length 2
			comparisons++;
			if(array[0] <= array[1]){
				return array;
			} else {
				return new int[] {array[1], array[0]};
			}
		} else {  // recurse onto sub-arrays of longer arrays
			int midpoint = array.length / 2;
			int[] bottom = sort(Arrays.copyOfRange(array, 0, midpoint));
			int[] top = sort(Arrays.copyOfRange(array, midpoint, array.length));
			// combine the sorted sub-arrays
			int i = 0;
			int j = 0;
			while(i < bottom.length && j < top.length){
				comparisons++;
				if(bottom[i] <= top[j]){
					array[i+j] = bottom[i];
					i++;
				} else {
					array[i+j] = top[j];
					j++;
				}
			}
			// one of the subarrays was fully copied; copy the other one
			if(i == bottom.length){
				for(; j < top.length; j++){
					array[i+j] = top[j];
				}
			} else {
				for(; i < bottom.length; i++){
					array[i+j] = bottom[i];
				}
			}

			return array;
		}
	}

	public static void main(String[] args){
		System.out.println("This program performs a merge sort on the list of integers given");
        if(args.length == 0){
            System.out.println("Usage: java MergeSort INT [INT…]");
            System.exit(0);
        }

        int[] array = new int[args.length];
        for(int i = 0; i < args.length; i++){
        	array[i] = Integer.parseInt(args[i]);
        }

        array = MergeSort.sort(array);

        StringBuilder resultString = new StringBuilder();
        resultString.append("The input array was sorted to [");
        for(int i = 0; i < array.length-1; i++){
        	resultString.append(new Integer(array[i]).toString()).append(" ");
        }
        resultString.append(new Integer(array[array.length-1]).toString());
        resultString.append("] after ").append(MergeSort.comparisons.toString()).append(" comparisons");
        System.out.println(resultString.toString());
	}
	
}
