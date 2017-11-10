library(ggplot2)
library(ggdendro)
library(ggfortify)
library(RColorBrewer)

make_expression_pca <- function(expr_m, cond_m, color_factor, shape_factor=NULL, size_factor=NULL, title=" ", custom_colors=NULL, 
                                custom_sizes=NULL, pca_axis1=1, pca_axis2=2, show_labels=F, label_size=3, default_size=5,
                                verbose=T, custom_names=NULL, label_shift_dist=2, color_text=F, only_text=F) {
    
    
    
    if (!all(colnames(expr_m) == cond_m[,"sample"])) {
        stop("Sample names and condition matrix are expected to be in same order, this didn't seem to be the case now")
    }

    tot_data <- plotPCA.custom(expr_m, cond_m, intgroup=c(color_factor, shape_factor, size_factor), returnData=TRUE, pcs = c(pca_axis1, pca_axis2))
    percentVar <- round(100 * attr(tot_data, "percentVar"))

    if (!is.null(custom_names)) {
        tot_data$name <- custom_names
    }
        
    if (missing(size_factor)) {
        size_val <- default_size
    }
    else {
        size_val <- size_factor
    }
    
    plt <- ggplot() 
        
    if (show_labels) {
        
        if (color_text) {
            plt <- plt + geom_text(data=tot_data, aes_string(label="name", x = tot_data[["PC1"]], y = tot_data[["PC2"]] - label_shift_dist, color=color_factor), size=label_size)
        }
        else {
            color <- "black"
            plt <- plt + geom_text(data=tot_data, aes_string(label="name", x = tot_data[["PC1"]], y = tot_data[["PC2"]] - label_shift_dist), size=label_size, color="black")
        }
    }
    
    if (!only_text) {
        if (!is.null(custom_sizes)) {
            plt <- plt + geom_point(data=tot_data, aes_string(x = tot_data[["PC1"]], y = tot_data[["PC2"]], color=color_factor, shape=shape_factor, size=size_val))
        }
        else {
            plt <- plt + geom_point(data=tot_data, aes_string(x = tot_data[["PC1"]], y = tot_data[["PC2"]], color=color_factor, shape=shape_factor), size=size_val)
        }
    }
    
    plt <- plt +
        xlab(paste0("PC", pca_axis1, ": ", percentVar[1], "% variance")) +
        ylab(paste0("PC", pca_axis2, ": ", percentVar[2], "% variance")) +
        ggtitle(title)
    
    if (!missing(custom_colors)) {
        plt <- plt + scale_color_manual(values=custom_colors)
    }


    if (!missing(custom_sizes)) {
        plt <- plt + scale_size_manual(values=custom_sizes)
    }
    
    return(plt)
    
}

plotPCA.custom <- function(expr_m, cond_m, intgroup="condition", ntop=500, returnData=TRUE, pcs = c(1,2), verbose=F) {
    
    # Edited version of the DESeq2 built-in plotPCA which allows for specifying specific PCAs
    
    # Check that number of PCs is two
    stopifnot(length(pcs) == 2)
   
    pca <- get_pca_object(expr_m, verbose=verbose)
    
    # the contribution to the total variance for each component
    percentVar <- pca$sdev^2 / sum( pca$sdev^2 )
    
    if (!all(intgroup %in% colnames(cond_m))) {
        stop("the argument 'intgroup' should specify columns of colnames(cond_m)")
    }
    
    intgroup.df <- as.data.frame(cond_m[, intgroup, drop=FALSE])
    
    # add the intgroup factors together to create a new grouping factor
    group <- if (length(intgroup) > 1) {
        factor(apply( intgroup.df, 1, paste, collapse=" : "))
    } 
    else {
        cond_m[[intgroup]]
    }
    
    # assembly the data for the plot (here we just use the pcs object passed by the end user)
    d <- data.frame(PC1=pca$x[,pcs[1]], PC2=pca$x[,pcs[2]], group=group, intgroup.df, name=rownames(cond_m))
    
    if (returnData) {
        attr(d, "percentVar") <- percentVar[pcs]
        return(d)
    }
}

plotMDS <- function(expr_m, labels, levels, comp1=1, comp2=2, title="no title") {
    
    warning("Warning: Be careful with this function. Make sure that labels are correctly synced with data. TODO: Make it order independent.")
  
    # if (!all(sort(colnames(expr_m)) == colnames(expr_m))) {
    #     stop("Sample names and condition matrix are expected to be in sorted order, this didn't seem to be the case now")
    # }
    
    d <- stats::dist(scale(t(stats::na.omit(expr_m)), center=TRUE, scale=TRUE))
    fit <- stats::cmdscale(d, eig=TRUE, k=2)
    x <- fit$points[, comp1]
    y <- fit$points[, comp2]
    graphics::plot(x, y, type="n", main=title, xlab="", ylab="")
    graphics::text(fit$points[, 1], fit$points[, 2], col=levels, labels=labels)
    # graphics::text(fit$points[, 1], fit$points[, 2], col=labels, labels=labels)
}


get_pca_object <- function(expr_m, verbose=F) {
    
    expr_m_nona <- expr_m[complete.cases(expr_m),]
    if (verbose) {
        print(paste("Dimensions before filtering:", paste(dim(expr_m), collapse=" ")))
        print(paste("Dimensions after filtering:", paste(dim(expr_m_nona), collapse=" ")))
    }
    pca <- prcomp(t(expr_m_nona), scale=TRUE, center=TRUE)
    
    # rv <- genefilter:::rowVars(assay(pca_object_data))
    # select <- order(rv, decreasing=TRUE)[seq_len(min(ntop, length(rv)))]
    # pca <- prcomp(t(assay(pca_object_data)[select,]))
    return(pca)
}

get_component_fraction <- function(expr_m) {
    
    # Retrieves a vector with percentage contributions for each PC
    
    pca_object <- get_pca_object(expr_m)
    
    percentVar <- pca_object$sdev^2 / sum(pca_object$sdev^2 )
    names(percentVar) <- colnames(pca_object$x)
    return(percentVar)
}

plot_component_fraction <- function(expr_m) {
    
    # Directly outputs the PCA numbers together with PC fractions
    
    comp_perc <- get_component_fraction(expr_m)
    plot(100 * comp_perc, main="PC loadings", xlab="PC", ylab="Perc. var")
}


generate_dendogram <- function(data_m, design_m, sort_names, color_names, label_names, pick_top_variance=null, title="Dendogram") {
    
    # Setup data
    colnames(data_m) <- design_m[, sort_names]
    expr_m_nona <- data_m[complete.cases(data_m),]
    rownames(design_m) <- as.character(design_m[, sort_names])
    
    # Calculate tree
    scaledTransposedMatrix <- scale(t(expr_m_nona), center=TRUE, scale=TRUE)
    hc <- stats::hclust(stats::dist(scaledTransposedMatrix), "ave")
    dhc <- as.dendrogram(hc)
    ddata <- dendro_data(dhc, type="rectangle")
    
    # Prepare for plotting
    reordered <- design_m[as.character(ddata$labels$label),]
    ddata$labels$color <- reordered[, color_names]
    ddata$labels$label <- reordered[, label_names]
    
    # Visualize
    plt <- ggplot(segment(ddata)) +
        geom_segment(aes(x=x, y=y, xend=xend, yend=yend)) +
        theme_dendro() +
        geom_text(data=label(ddata), 
                  aes(x=x, y=y, label=label, color=color), 
                  vjust=0.5, hjust=0, size=3) +
        coord_flip() + 
        scale_y_reverse(expand=c(0.2, 0)) +
        scale_x_continuous(expand=c(0,1)) +
        ggtitle(title) +
        theme(legend.position="none")
    
    options(repr.plot.width=14, repr.plot.height=14)
    plt
}



# get_top_contributing_genes <- function(pca_object, target_pc) {
#     
#     # Retrieves genes with loadings for which the loading has the highest impact on the target PC
#     
#     pca_names <- colnames(pca_object$x)
#     ordered <- order(abs(pca_object$rotation[,target_pc]), decreasing=TRUE)
#     target_loadings <- pca_object$rotation[,target_pc][ordered]
#     return(target_loadings)
# }
# 
# print_top_contributing_genes <- function(pca_object, target_pc, number_to_print=20) {
#     
#     # Prints a subset of the top contributing genes
#     
#     gene_list <- get_top_contributing_genes(pca_object, target_pc)
#     
#     for (gene_name in head(names(gene_list), number_to_print)) {
#         print(noquote(paste(gene_name, gene_list[gene_name])))
#     }
# }

