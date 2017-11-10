library(limma)

calculate_anova_table <- function(df, header) {
    do_anova <- function(row_values) {
        summary(stats::aov(row_values~header))[[1]][[5]][1]
    }
    
    p_values <- apply(df, 1, do_anova)
    fdr_values <- p.adjust(p_values, "BH")
    sign_table <- cbind(anova_p=p_values, anova_fdr=fdr_values)
    sign_table
}


calc_corr_column <- function(df, ref_levels, method="spearman") {
    
    valids <- c("spearman", "pearson")
    
    if (!method %in% valids) {
        stop(paste("Unknown correlation method: ", method))
    }
    
    corr_vals <- apply(df, 1, function(row) { cor(x=ref_levels, y=row, method=method, use="complete.obs") })
}


# Filters out rows where a given number of values isn't present
# in all replicate groups
filter_low_rep <- function(df, groups, least_rep=2) {
    
    row_meet_thres_contrast <- apply(df, 1, all_replicates_have_values, groups=groups, min_count=least_rep)
    filtered_df <- df[row_meet_thres_contrast, ]
}


all_replicates_have_values <- function(row, groups, min_count) {
    names(row) <- groups
    rep_counts <- table(names(na.omit(row)))
    length(rep_counts) == length(unique(groups)) && min(rep_counts) >= min_count
}

get_limma_fit <- function(data_df, header, design_names, my_contrasts) {
    
    design <- model.matrix(~0+header)
    
    colnames(design) <- design_names
    matrix <- data.matrix(data_df)
    
    contrast.matrix <- makeContrasts(contrasts=my_contrasts, levels=design)
    
    fit <- lmFit(matrix, design)
    fit2 <- contrasts.fit(fit, contrast.matrix)
    fit2 <- eBayes(fit2)
    
    fit2
}

get_limma_table <- function(limma_fit, coef) {
    topTable(limma_fit, coef=coef, number=Inf, sort.by="none")
}

show_limma_venn <- function(limma_fit, adjustment, thres, title) {
    results <- decideTests(limma_fit, adjust.method=adjustment, p.value=thres)
    vennDiagram(results, 
                include=c("up", "down"), 
                counts.col=c("red", "blue"), 
                circle.col = c("red", "blue", "green3"),
                main=title,
                cex=c(1,0.7,0.4),   # Scaling of large, medium and small text in plot
                mar=c(0,0,1.5,0))
}




