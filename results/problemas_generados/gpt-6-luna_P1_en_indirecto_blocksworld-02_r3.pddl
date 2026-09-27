(define (problem blocks-tower)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (on c b)
    (ontable b)
    (clear c)
    (ontable a)
    (clear a)
    (ontable d)
    (clear d)
    (handempty)
  )
  (:goal (and
    (on a b)
    (on b c)
    (on c d)
  ))
)
