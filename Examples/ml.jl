println("reminder to Russell")
println("to install packages use")
println("launch julia using sudo")
println("try to import module first using, 'using'")
println("include('ml.jl')")
#println("Pkg.add('PyCall')")
println("\n\n\n\n\n\n")

function trypy()
	try
        ENV["PYTHON"] = "/anaconda3/bin/python"

        Pkg.test("PyCall")
        plt = pyimport("matplotlib.pyplot")

		#return unreliable_connect()
	catch ex
        ENV["PYTHON"] = "/opt/conda/bin/python"
        Pkg.test("PyCall")
        math = pyimport("math")
        math.sin(math.pi / 4) # returns ≈ 1/√2 = 0.70710678...
   end
end
try
	using Knet
	using PyCall
    using Plots;
    using StatsPlots;
    using DataFrames
    using IJulia
	using PyPlot
	using Plots
	using GR


catch
    using Pkg
	#Pkg.rm("StatPlots")
	Pkg.add("StatsPlots")
	#Pkg.add("Gallium")
	Pkg.add("GR")
    Pkg.add("IJulia")
    Pkg.add("Plots")
    Pkg.add("StatsPlots") #to install the StatPlots package.
    Pkg.add("DataFrames")
	Pkg.add("Seaborn")
	Pkg.add("PyPlot")

    using DataFrames
    using IJulia
	using Knet
    using Plots;
    using StatsPlots;
    using PyCall
end

@pyimport pickle
f = pybuiltin("open")("scraped_new.p","rb")
p = pickle.Unpickler(f)
scraped_new = p[:load]()
f[:close]()
scraped_new[1]["wcount"]
wc = [ sn["wcount"] for sn in scraped_new ]
sp = [ sn["sp"] for sn in scraped_new ]
#subjectivity = [ sn["ss"] for sn in scraped_new ]
features = {}
features = Dict()
subjectivity = [ sn["ss"] for sn in scraped_new if haskey(sn,"ss") ]
features["ss"] = subjectivity
features["ss"] = wc
features["sp"] = sp

#var	info(sn)
gr()
histogram(sn)
#using PyPlot
#h = PyPlot.plt.hist(sn)
png("document_length_distribution.png")
varinfo()
f = pybuiltin("open")("big_model_science.p","rb")
p = pickle.Unpickler(f)
bms = p[:load]()
f[:close]()

# ArtCorpus
with open('traingDats.p','rb') as f:
	trainingDats = pickle.load(f)


#=

	include(Knet.dir("data","housing.jl"));
	x,y = housing();

	predict(w, x) = w[1] * x .+ w[2];
	loss(w, x, y) = mean(abs2, predict(w, x)-y);
	lossgradient = grad(loss);

	function train(w, data; lr=0.01)
	    for (x,y) in data
	        dw = lossgradient(w, x, y)
	        for i in 1:length(w)
	            w[i] -= dw[i]*lr
	        end
	    end
	    return w
	end;

	#plotly();
	gr();
	scatter(x', y[1,:], layout=(3,5), reg=true, size=(950,500))
	savefig("dnn_scatter_plot.png")
	w = Any[ 0.1*randn(1,13), 0.0 ];
	errdf = DataFrame(Epoch=1:20, Error=0.0);
	#BigInt cntr;

	println("try to import module first using, 'using'")
	#println("Pkg.add('PyCall')")
	println("\n\n\n\n\n\n")

	for i=1:200
		cntr = 1
		#println("cntr",cntr)

	    println(i,cntr)
	    train(w, [(x,y)])
	    if mod(i, 10) == 0
	        println("Epoch $i: $(round(loss(w,x,y)))")
	        errdf[cntr, :Epoch]=i
	        errdf[cntr, :Error]=loss(w,x,y)
	        cntr+=1
	    end
	end;
	print(errdf)

=#

#exit();
